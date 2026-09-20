import json
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


PROVIDER_CONFIG_PATH = Path(__file__).with_name("provider_config.json")


def load_provider_config(config_path=PROVIDER_CONFIG_PATH):
    with open(config_path, encoding="utf-8") as file:
        return json.load(file)


def get_nested_value(payload, path):
    value = payload

    for key in path:
        value = value[key]

    return value


def normalize_tee_time(raw_tee_time, provider_config):
    field_map = provider_config["field_map"]
    raw_time = raw_tee_time[field_map["time"]]
    normalized_time = datetime.strptime(
        raw_time,
        provider_config["time_input_format"],
    ).strftime(provider_config["time_output_format"]).lstrip("0")

    return {
        "time": normalized_time,
        "available": raw_tee_time[field_map["available"]],
        "players_available": raw_tee_time[field_map["players_available"]],
    }


def normalize_tee_sheet(raw_tee_sheet, provider_config):
    normalized_tee_times = []

    for raw_tee_time in raw_tee_sheet:
        normalized_tee_time = normalize_tee_time(
            raw_tee_time,
            provider_config,
        )
        normalized_tee_times.append(normalized_tee_time)

    return normalized_tee_times


def get_tee_times(provider_config_path=PROVIDER_CONFIG_PATH):
    provider_config = load_provider_config(provider_config_path)
    captured_tee_times = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        def capture_response(response):
            response_url_contains = provider_config["response_url_contains"]

            if response_url_contains in response.url:
                payload = response.json()
                raw_tee_sheet = get_nested_value(
                    payload,
                    provider_config["tee_times_path"],
                )
                normalized_tee_sheet = normalize_tee_sheet(
                    raw_tee_sheet,
                    provider_config,
                )
                captured_tee_times.extend(normalized_tee_sheet)

        page.on("response", capture_response)
        page.goto(provider_config["start_url"])

        print("Complete authentication and open a tee-time page in the browser.")

        while not captured_tee_times:
            page.wait_for_timeout(500)

        browser.close()

    return captured_tee_times
