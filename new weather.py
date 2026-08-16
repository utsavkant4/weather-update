import requests
import csv
import os
from datetime import datetime

API_KEY = "ae0691164a49c752dfeeea43a7cd896d"

# Bihar ke districts/cities - jitni chaho utni add/remove kar sakte ho
CITIES = [
    "Samastipur", "Araria", "Arwal", "Aurangabad", "Banka",
    "Begusarai", "Bhagalpur", "Arrah", "Buxar", "Darbhanga",
    "Mothihari", "Gaya", "Gopalganj", "Jamui", "Jehanabad",
    "Bhabhua", "Katihar", "Khagaria", "Kishanganj", "Lakhisarai",
    "Madhepura", "Madhubani", "Munger", "Muzaffarpur", "Nalanda",
    "Nawada", "Patna"
]

import os

# Desktop ke andar "data" folder mein save hoga
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "data")
os.makedirs(DESKTOP_PATH, exist_ok=True)  # agar folder nahi hai to bana dega

CSV_FILE = os.path.join(DESKTOP_PATH, "weather_data.csv")

FIELDNAMES = ["City", "Temperature", "Feels Like", "Humidity", "Condition", "Wind Speed", "Time"]


def fetch_weather(city):
    """Fetch current weather for a city from OpenWeatherMap."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "City": data["name"],
            "Temperature": data["main"]["temp"],
            "Feels Like": data["main"]["feels_like"],
            "Humidity": data["main"]["humidity"],
            "Condition": data["weather"][0]["description"],
            "Wind Speed": data["wind"]["speed"],
            # IMPORTANT: consistent format every time, no mixing formats
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    else:
        print(f"⚠️ Failed to fetch data for {city}: {response.status_code}")
        return None


def save_to_csv(records):
    """Append records to CSV, creating the file with headers if it doesn't exist."""
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        for record in records:
            writer.writerow(record)


def run():
    records = []
    for city in CITIES:
        record = fetch_weather(city)
        if record:
            records.append(record)
            print(f"✅ {record['City']} | {record['Temperature']}°C | {record['Condition']} | {record['Time']}")

    save_to_csv(records)
    print(f"\n📁 Saved {len(records)} records to {CSV_FILE}")


if __name__ == "__main__":
    run()