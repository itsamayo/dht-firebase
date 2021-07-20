### DHT script for posting updates to Firebase Realtime DB  

### Setup  

1. Create a `config.json` file in the root using the `example.config.json` as a template

2. Create a `firebase-secret.json` in the root using a Firebase generated JSON for the Admin SDK found [here](https://console.firebase.google.com/u/0/project/pi-office-d68fc/settings/serviceaccounts/adminsdk)
3. Run the below:
```
# Execute with python 3.6+ compatible pip

$ pip3 install requirements.txt
```  

### Usage  

```
# Execute with python 3.6+

python3 main.py 
```  

### Fix potential issues on installing admin-firebase with pip

```
pip3 install --update setuptools

sudo apt-get install libffi-dev
```