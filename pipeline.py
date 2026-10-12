import requests
import sqlite3


LATITUDE = 41.01 #for istanbul
LONGITUDE = 28.98


def extract():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def transform(raw):
    current = raw["current"]
    return {
        "observed_at": current["time"],
        "temperature_c": current["temperature_2m"],
        "humidity_pct": current["relative_humidity_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
    }


def load(row):
    conn = sqlite3.connect("weather.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            observed_at TEXT,
            latitude REAL,
            longitude REAL,
            temperature_c REAL,
            humidity_pct REAL,
            wind_speed_kmh REAL,
            UNIQUE (observed_at, latitude, longitude)
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO weather
        (observed_at, latitude, longitude, temperature_c, humidity_pct, wind_speed_kmh)
        VALUES (:observed_at, :latitude, :longitude, :temperature_c, :humidity_pct, :wind_speed_kmh)
    """, row)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    raw = extract()
    row = transform(raw)
    load(row)
    print("Saved:", row)