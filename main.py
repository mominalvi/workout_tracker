import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app_id = os.environ.get("APP_ID")
api_key = os.environ.get("API_KEY")
token = os.environ.get("TOKEN")

bearer_headers = os.environ["BEARER"]

headers = {
    "x-app-id": app_id,
    "x-app-key": api_key,
    "x-remote-user-id": "1",
    "Authorization": f"Bearer {token}"
}

user_query = input("Tell me which exercises you did: ")

exercise_params = {
    "query": user_query,
    "gender":"male",
    "weight_kg":70,
    "height_cm":170,
    "age":18
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
data = response.json()

sheets_endpoint = os.environ["SHEET_ENDPOINT"]
date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().time().strftime('%H:%M:%S')

for exercise in data["exercises"]:
    sheety_params = {
        "workout": {
            "d": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheety_response = requests.post(url=sheets_endpoint, json=sheety_params, headers=headers)
    print(sheety_response.text)


