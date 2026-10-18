# Weather Pipeline

A small ETL pipeline that pulls current weather data from the Open-Meteo API, cleans it with Python, and stores it in a SQLite database. A GitHub Actions workflow runs it every day.

## How it works

Open-Meteo API → Python (extract and transform) → SQLite (`weather.db`)

- `pipeline.py` fetches temperature, humidity and wind speed, renames the fields, and saves one row per observation.
- The table has a unique rule on time and location, so running the script twice doesn't create duplicates.
- `.github/workflows/daily.yml` runs the script every day at 06:00 UTC and commits the updated `weather.db` back to the repo.

## Run it yourself

```
pip install -r requirements.txt
python pipeline.py
```

The city is set by the `LATITUDE` and `LONGITUDE` values at the top of `pipeline.py`.

## Limitations

Committing a database file to Git is fine for a demo, but a real pipeline would write to a hosted database.
