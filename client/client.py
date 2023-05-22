from datetime import datetime
import requests
import json
import time
import random
import pytz

APP_NAME = "monitoring-app"
APP_ENDPOINT= f"http://{APP_NAME}:5000/data"
TIMEZONE = pytz.timezone('Europe/Paris')

while True:
    temperature = round(random.uniform(10, 40), 2)
    humidity = round(random.uniform(20, 80), 2)
    luminosity = round(random.uniform(0, 100), 2)
    timestamp_str = datetime.now(TIMEZONE).strftime('%d-%m-%Y %H:%M:%S')
  
    data = {
        "temperature": str(temperature),
        "humidity": str(humidity),
        "luminosity": str(luminosity),
        "timestamp": timestamp_str
    }
    
    headers = {'Content-type': 'application/json'}
    r = requests.post(APP_ENDPOINT, data=json.dumps(data), headers=headers)
    print("Data sent to serverless function:", r.text)
    
    time.sleep(30)