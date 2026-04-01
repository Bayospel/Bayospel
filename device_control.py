# device_control.py
import ppadb.client as adb

def connect_to_device():
 client = adb.Client(host="127.0.0.1", port=5037)
 devices = client.devices()
 if devices:
 return devices[0]
 else:
 print("No devices found")
 return None

def send_command(device, command):
 device.shell(command)

if __name__ == "__main__":
 device = connect_to_device()
 if device:
 send_command(device, "input keyevent 26") # Example: Lock the screen

