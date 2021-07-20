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
cred = credentials.Certificate('./firebase-secret.json')
ref = db.reference(config()['ROOT'] + config()['COLLECTION_ID'])
data = ref.child(config()['DATA_TITLE'])

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': config()['FIREBASE_DATABASE_URL']
})

# Call made to Firebase realtime DB
def updateDB(temp, humidity):
    timestamp = time.time()
    data.update({
        id: {
            'temp': temp,
            'humidity': humidity,
            'timestamp': int(timestamp)
        }
    })

# Polling loop for sensor
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        updateDB(temperature, humidity)
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(config()['POLLING_INTERVAL'])