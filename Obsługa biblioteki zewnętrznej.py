import requests
from datetime import datetime, timedelta
import os


LATITUDE = 52.17
LONGITUDE = 16.44
CACHE_FILE = "weather.txt"

def date_from_user():
    user_input = input("Podaj datę (YYYY-MM-DD) lub ENTER aby sprawdzić jutro: ").strip()
    if user_input == "":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        datetime.strptime(user_input, "%Y-%m-%d")
        return user_input
    except ValueError:
        print("Nieprawidłowy format daty!")
        exit(1)


def read_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                date, result = line.strip().split("|")
                cache[date] = result
    return cache


def save_to_cache(date, result):
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date}|{result}\n")


def rain_from_api(date):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&daily=rain_sum"
        "&timezone=Europe%2FLondon"
        f"&start_date={date}"
        f"&end_date={date}"
    )

    response = requests.get(url)
    data = response.json()

    try:
        rain = data["daily"]["rain_sum"][0]
        if rain > 0:
            return "Będzie padać"
        elif rain == 0:
            return "Nie będzie padać"
        else:
            return "Nie wiem"
    except (KeyError, IndexError, TypeError):
        return "Nie wiem"



date = date_from_user()
cache = read_cache()

if date in cache:
    print(cache[date])
else:
    result = rain_from_api(date)
    save_to_cache(date, result)
    print(result)