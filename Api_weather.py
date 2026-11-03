import requests
import pandas as pd
import os
from datetime import datetime

API_KEY = "ae0691164a49c752dfeeea43a7cd896d"

CITY = [
    "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur",
    "Arrah", "Buxar", "Darbhanga", "Motihari", "Gaya", "Gopalganj",
    "Jamui", "Jehanabad", "Bhabua", "Katihar", "Khagaria", "Kishanganj",
    "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur",
    "Nalanda", "Nawada", "Patna", "Purnia", "Sasaram", "Saharsa",
    "Samastipur", "Chapra", "Sheikhpura", "Sheohar", "Sitamarhi",
    "Siwan", "Supaul", "Hajipur", "Bettiah"
]

all_weather = []

for city in CITY:

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        weather = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "City": data["name"],
            "Temperature": data["main"]["temp"],
            "Feels Like": data["main"]["feels_like"],
            "Humidity": data["main"]["humidity"],
            "Condition": data["weather"][0]["description"],
            "Wind Speed": data["wind"]["speed"]
        }

        all_weather.append(weather)

        print(
            f"✅ {city}: "
            f"{weather['Temperature']}°C, "
            f"{weather['Condition']}"
        )

    else:
        print(f"⚠️ Failed for {city}: {response.status_code}")


if all_weather:

    df = pd.DataFrame(all_weather)

    file = "weather_data.csv"

    # Keep the same column order as existing CSV
    if os.path.exists(file):

        old_columns = pd.read_csv(file, nrows=0).columns.tolist()

        df = df[old_columns]

        # Append new data without writing headers again
        df.to_csv(
            file,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig"
        )

    else:
        df.to_csv(
            file,
            index=False,
            encoding="utf-8-sig"
        )

    print(f"\n {len(all_weather)} cities added to {file}")

else:
    print("\n No data was fetched.")