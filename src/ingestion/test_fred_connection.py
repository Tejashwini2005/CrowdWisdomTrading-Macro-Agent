
"""Test the FRED API connection with one economic observation."""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FRED_API_KEY")
API_URL = "https://api.stlouisfed.org/fred/series/observations"

def main():
    if not API_KEY:
        print("FRED_API_KEY is missing from .env")
        sys.exit(1)

    params = {
        "series_id": "UNRATE",
        "api_key": API_KEY,
        "file_type": "json",
        "limit": 1,
        "sort_order": "desc",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        observations = data.get("observations", [])
        if not observations:
            print("Connected, but no observations were returned.")
            return

        item = observations[0]
        print("FRED API connection successful.")
        print(f"Series: UNRATE (US unemployment rate)")
        print(f"Latest returned observation date: {item['date']}")
        print(f"Value: {item['value']}")
        print("API key was not displayed.")

    except requests.RequestException as exc:
        print(f"FRED request failed: {type(exc).__name__}")
        print("Check your internet connection and FRED API key.")
        sys.exit(1)
    except ValueError:
        print("FRED returned an unexpected response. Check the API key and response.")
        sys.exit(1)

if __name__ == "__main__":
    main()
