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

cred = credentials.Certificate('./firebase-secret.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': config()['FIREBASE_DATABASE_URL']
})

# DB Related
ref = db.reference(config()['ROOT'] + config()['COLLECTION_ID'])
data = ref.child(config()['DATA_TITLE'])
statusData = ref.child('status')

# Calls made to Firebase realtime DB

# Module Data
def updateModuleData(temp, humidity):
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    timestamp = time.time()
    data.update({
        id: {
            'temp_celcius': temp,
            'humidity_percent': humidity,
            'timestamp_epoch': int(timestamp)
        }
    })

# Sensor Status
def updateModuleStatus(status):
    id = 'status'
    statusData.update({status})

# Polling loop for sensor
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        updateModuleData(temperature, humidity)
        updateModuleStatus("online")
    else:
        print("Sensor failure. Check wiring.")
        updateModuleStatus("offline")        
    time.sleep(config()['POLLING_INTERVAL'])