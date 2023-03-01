# Written by K. M. Knausgård 2023-03-01.
#
# Set environment variables cmx_server, cmx_user, cmx_password, and device_hw_addr before use.
#
import os
import requests
import numpy as np
import matplotlib.pyplot as plt

m2f = 3.281
f2m = 1/m2f

protocol = "https://"
server = os.environ["cmx_server"]
api = "/api/location/v3/clients"

device_hw_addr = os.environ["device_hw_addr"]


def fetch_device_position(hw_addr):
    print(protocol + server + api)
    r = requests.get(protocol + server + api,
                     auth=(os.environ["cmx_user"], os.environ["cmx_password"]), params={"macAddress": hw_addr})
    print(r.text)

    data = r.json()
    if len(data) < 1:
        print("No valid response.")
        return

    coordinates = data[0].get("locationCoordinate")
    if coordinates is None:
        print("No valid coordinates in response")
        return
    print(coordinates)
    print(coordinates.get("x"))

    return np.array([coordinates.get("x"), coordinates.get("y")]) * f2m


def main():
    #fig = plt.figure()
    fig, ax = plt.subplots(1)
    ax.set(xlim=(50, 90), ylim=(25, 100))
    ax.set_title("Device " + device_hw_addr + " position.")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid()

    # Log @ 1 SPS for approx. 60s
    for i in range(60):
        pos = fetch_device_position(device_hw_addr)
        #pos = np.array([42.0*2, 31.415926])
        if pos is None:
            print("Device not found (not there or no network connection).")
            return
        ax.scatter(pos[0], pos[1])
        plt.pause(1.00)

    plt.show()


if __name__ == '__main__':
    main()
