from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, firestore

# constants
COLLECTION = 'raspberry'
DOCUMENT = 'dashboard'

# firebase
cred = credentials.Certificate("./config/iotlabo-py-firebase-adminsdk-l8p22-a2192e623f.json")
firebase_admin.initialize_app(cred)

# sensehat 
sense = SenseHat()
sense.set_imu_config(False, False, False)
sense.clear()

def hex_to_rgb(hex):
     return tuple(int(hex[i:i+2], 16) for i in (0,2,4)) 

def update_sensehat(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_readable = doc.to_dict()

        value = doc_readable['matrix']['color']['value']
        status = doc_readable['matrix']['isOn']

        rgb = hex_to_rgb(value)
        print(rgb)
        
        if status == True :
            sense.clear(rgb)
        else :
            sense.clear()

# connect firestore
db = firestore.client()
pi_ref = db.collection(COLLECTION).document(DOCUMENT)
pi_watch = pi_ref.on_snapshot(update_sensehat)

# app
while True:
    pass
