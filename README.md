# Golf Tee-Time Monitor

**Status: Active Development**

Golf Tee-Time Monitor is a provider-configurable Python prototype. It opens a
visible browser, waits for manual authentication and navigation, captures a
configured tee-time JSON response, normalizes the returned records, checks for
exact target-time and player-count matches, and prints matching alerts in the
terminal.

The public project intentionally excludes real provider URLs, private response
markers, provider payload fields, credentials, cookies, and browser-session
state.

## Current functionality

- Launches Chromium through Playwright in visible mode.
- Allows the user to authenticate and navigate manually.
- Listens for a locally configured network-response URL substring.
- Extracts a tee-time list through a locally configured JSON path.
- Maps provider fields into a standard structure:
  `time`, `available`, and `players_available`.
- Converts provider time strings into the display format expected by the app.
- Checks exact target times, availability, and minimum player capacity.
- Prints a terminal alert for each matching tee time.

## Roadmap

### Current — Implemented

- Live tee-time response capture through Playwright
- Manual authentication and tee-sheet navigation
- Provider-configurable JSON parsing and normalization
- Target-time and player-count filtering
- Terminal availability alerts

### Next — Planned

- Configurable time-window matching
- Automatic date selection
- Persistent authenticated sessions
- Continuous availability monitoring

### Later — Planned

- Reservation workflow exploration
- Duplicate-action and verification safeguards
- External notifications
- User interface / packaged application

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the Python dependency and Chromium:

   ```bash
   python -m pip install -r requirements.txt
   python -m playwright install chromium
   ```

3. Create local configuration files from the safe examples:

   ```bash
   cp config.example.json config.json
   cp provider_config.example.json provider_config.json
   ```

4. Edit `config.json` with target times and the minimum number of players:

   ```json
   {
     "target_times": ["9:00 AM", "9:30 AM"],
     "players": 1
   }
   ```

5. Edit `provider_config.json` with details for a service you are authorized to
   access. The local provider configuration contains:

   - `start_url`: the page opened when the browser launches.
   - `response_url_contains`: text identifying the relevant network response.
   - `tee_times_path`: the sequence of JSON keys leading to the tee-time list.
   - `field_map`: provider field names for time, availability, and open spots.
   - `time_input_format`: the provider's time format.
   - `time_output_format`: the normalized display format.

   Both local configuration files are ignored by Git. Do not commit real
   provider details, credentials, captured responses, or session data.

## Run

```bash
python main.py
```

The program opens Chromium. Complete authentication manually, navigate to the
desired tee-time page, and trigger the configured response. After the response
is captured, the browser closes and the program prints any exact matches.

## Sample data

`sample_tee_times.json` is a fictional example of the normalized record shape.
It is not used by the current live execution path.

## Current limitations

- Authentication and tee-sheet navigation are manual.
- Provider details and JSON mappings must be supplied locally.
- Target-time matching is exact; there is no configurable time window.
- The program handles one captured tee sheet per run.
- There is no automatic date selection, continuous monitoring, retry/timeout
  workflow, persistent login, reservation or booking workflow, GUI, or external
  notification system.
- Compatibility depends on an authorized provider exposing a suitable JSON
  response that can be described by the local configuration.

Use this project only with services and accounts you are authorized to access,
and follow the provider's applicable rules and terms.

## Project files

- `main.py`: loads user preferences, evaluates normalized tee times, and prints
  alerts.
- `provider_client.py`: launches the browser, captures the configured response,
  and normalizes provider records.
- `config.example.json`: safe example of the user preference schema.
- `provider_config.example.json`: fictional example of the provider mapping
  schema.
- `sample_tee_times.json`: fictional normalized records for reference.
