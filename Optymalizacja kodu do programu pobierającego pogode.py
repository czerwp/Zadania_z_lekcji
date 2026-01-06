import os
import json
from datetime import datetime, timedelta
import requests

class WeatherForecast:
    def __init__(self, latitude, longitude, cache_file="weather_cache.json"):
        self.latitude = latitude
        self.longitude = longitude
        self.cache_file = cache_file
        self._data = {}
        self._load_cache()
        self._iter_index = 0
        self._keys = list(self._data.keys())

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}

    def _save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False)

    def _query_api(self, date):
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.latitude}"
            f"&longitude={self.longitude}"
            "&daily=rain_sum"
            "&timezone=Europe%2FLondon"
            f"&start_date={date}"
            f"&end_date={date}"
        )
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            rain = data.get("daily", {}).get("rain_sum", [None])[0]
            if rain is None or rain < 0:
                return "Nie wiem"
            elif rain > 0:
                return "Będzie padać"
            else:
                return "Nie będzie padać"
        except Exception:
            return "Nie wiem"

    def __setitem__(self, date, value):
        self._data[date] = value
        self._save_cache()

    def __getitem__(self, date):
        if date in self._data:
            return self._data[date]
        else:
            result = self._query_api(date)
            self._data[date] = result
            self._save_cache()
            self._keys = list(self._data.keys())
            return result

    def __iter__(self):
        self._keys = list(self._data.keys())
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self._keys):
            date = self._keys[self._iter_index]
            self._iter_index += 1
            return date
        else:
            raise StopIteration

    def items(self):
        for date, value in self._data.items():
            yield (date, value)

if __name__ == "__main__":
    latitude = 52.17
    longitude = 16.44

    wf = WeatherForecast(latitude, longitude)

    user_input = input("Podaj datę (YYYY-MM-DD) lub ENTER aby sprawdzić jutro: ").strip()
    if user_input == "":
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            date = user_input
        except ValueError:
            print("Nieprawidłowy format daty!")
            exit(1)
    result = wf[date]
    print(f"Pogoda dla {date}: {result}")
    print("\n Historia:")
    for d, r in wf.items():
        print(d, r)
    print("\n Zapisane daty:")
    for d in wf:
        print(d)