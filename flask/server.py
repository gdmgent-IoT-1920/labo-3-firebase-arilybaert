# import libraries
from flask import Flask, render_template, request
from sense_hat import SenseHat

# sensehat instantiëren
sense = SenseHat()
sense.set_rotation(180)
sense.set_imu_config(False, False, False)  # gyroscope only

# flask server instantiëren
app = Flask(__name__)

sense_values = {
    'value': '#000000',
    'type': 'hex',
    'message': ''
}

# function: on_snapshot(doc_snapshot, changes, read_time)
def convertHexValueToTuple(hex_value, list = False):
    r = int(hex_value[1:3], 16)
    g = int(hex_value[3:5], 16)
    b = int(hex_value[5:], 16)
    if(list):
        return [r, g, b]   
    return (r, g, b)

def colorTheMatrix():
    rgb_value = convertHexValueToTuple(sense_values['value'])
    sense.clear(rgb_value)

def messageOnMatrix():
    rgb_value = convertHexValueToTuple(sense_values['value'], True)
    sense.show_message(sense_values['message'], text_colour=rgb_value)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/hello')
def hello():
    return 'You have reached the Pi of F-Rogers'

@app.route('/sensehat', methods=['GET', 'POST'])
def sensehat():
    if(request.method == 'POST'):
        sense_values['value'] = request.form['senseColor']
        sense_values['message'] = request.form['message']
    if(sense_values['message'] == ''):
        colorTheMatrix()
    else:
        messageOnMatrix()

    return render_template('sensehat.html.j2', sense_values = sense_values)



# server constants
host = '10.120.145.2'
port = 8080
if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)