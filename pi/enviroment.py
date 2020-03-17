from sense_hat import SenseHat
import firebase_admin
import time
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



def get_set_value():

    # GET VALUE FROM SENSOR
    t = round(sense.get_temperature())
    p = round(sense.get_pressure())
    h = round(sense.get_humidity())

    # SET VALUES IN FB
    pi_ref.update(
        {'enviroment': {
            't' : t,
            'p' : p,
            'h' : h
        }},
        )
    sense.show_message(str(t), text_colour=[255, 100, 100])
    print(t)
    return [t, p, h]

# http://yaab-arduino.blogspot.com/2016/08/automatic-orientation-of-sense-hat-display.html
def auto_rotate_display():
  # read sensors data to detect orientation
  x = round(sense.get_accelerometer_raw()['x'], 0)
  y = round(sense.get_accelerometer_raw()['y'], 0)

  rot = 0
  if x == -1:
    rot=90
  elif y == -1:
    rot=180
  elif x == 1:
    rot=270
  # rotate the display according to the orientation
  sense.set_rotation(rot)

# connect firestore
db = firestore.client()
pi_ref = db.collection(COLLECTION).document(DOCUMENT)

# app
while True:
    auto_rotate_display()
    get_set_value()
    time.sleep(1)
