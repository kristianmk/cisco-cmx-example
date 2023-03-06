# Written by K. M. Knausgård 2022-03-02
# pip install simple-websocket
import os
import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


m2f = 3.281
f2m = 1/m2f

protocol = "https://"
server = os.environ["cmx_server"]
api = "/api/location/v3/clients"

device_hw_addr = os.environ["device_hw_addr"]


async_mode = None
app = Flask(__name__)
app.config["SECRET_KEY"] = "NotThatSecretKey"

socketio = SocketIO(app, sync_mode=async_mode)


def fetch_device_position(hw_addr):
    print(protocol + server + api)
    r = requests.get(protocol + server + api,
                     auth=(os.environ["cmx_user"], os.environ["cmx_password"]),
                     params={"macAddress": hw_addr})
    print(r.text)

    data = r.json()
    if len(data) < 1:
        print("No valid response.")
        return

    coordinates = data[0]["geoCoordinate"]
    print(data[0].get("confidenceFactor"))
    coordinates["confidenceFactor"] = data[0]["confidenceFactor"]*f2m  # Radius of 95% probability

    if coordinates is None:
        print("No valid coordinates in response")
        return
    print(coordinates)

    return coordinates


@socketio.on('request_geo_position')
def cmx_position(message):
    print("CMX position for " + device_hw_addr + " :")
    coordinates = fetch_device_position(device_hw_addr);
    emit('geo_position', coordinates)


@app.route("/")
def mazemap():  # name=None
    return render_template('mazemap.html', sync_mode=socketio.async_mode)


@socketio.on('custom_event')
def handle_custom_event(json):
    print('Received json: ' + str(json))


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)
