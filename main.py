import json
from provider_client import get_tee_times


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)

    return config


def is_matching_tee_time(tee_time, config):
    time_matches = tee_time["time"] in config["target_times"]
    is_available = tee_time["available"]
    enough_players = tee_time["players_available"] >= config["players"]

    return time_matches and is_available and enough_players


def main():
    config = load_config()
    tee_times = get_tee_times()

    print("Golf Tee-Time Monitor")
    print("---------------------")
    print("Target times:", config["target_times"])
    print("Players needed:", config["players"])
    print()
    print("Checking tee times...")

    match_found = False

    for tee_time in tee_times:
        if is_matching_tee_time(tee_time, config):
            print(
                f"ALERT: {tee_time['time']} is open for "
                f"{tee_time['players_available']} players!"
            )
            match_found = True

    if not match_found:
        print("No matching tee times found")


main()
