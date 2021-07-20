import firebase_admin
import Adafruit_DHT
import json
import time
import string
import random

from firebase_admin import credentials
from firebase_admin import db

def config():
    with open('./config.json', "r") as f:
        return json.load(f)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = config()['DHT_PIN']

# Data vars
id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# DB Related
cred = credentials.Certificate('./pi-office-secret.json')
ref = db.reference('pi/dht')
temp_hum_data = ref.child('temp_hum_data')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pi-office-d68fc-default-rtdb.firebaseio.com/'
})

def updateDB(temp, humidity):
    timestamp = time.time()
    temp_hum_data.update({
        id: {
            'temp': temp,
            'humidity': humidity,
            'timestamp': int(timestamp)
        }
    })

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        updateDB(temperature, humidity)
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(3)