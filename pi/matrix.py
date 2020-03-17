from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, firestore

# constants
COLLECTION = 'raspberry_collection'
DOCUMENT = 'lectorpi_doc'

# firebase
cred = credentials.Certificate("./config/iotlabo-85706-firebase-adminsdk-wd3oa-d11daf23ba.json")
firebase_admin.initialize_app(cred)

# sensehat 
sense = SenseHat()
sense.set_imu_config(False, False, False)
sense.clear()

def update_sensehat(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_readable = doc.to_dict()
        print(doc_readable)

# connect firestore
db = firestore.client()
pi_ref = db.collection(COLLECTION).document(DOCUMENT)
pi_watch = pi_ref.on_snapshot(update_sensehat)

# app
while True:
    pass
