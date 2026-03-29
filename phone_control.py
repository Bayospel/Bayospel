from ppadb.client import Client as AdbClient

def connect_phone():
    # Start the ADB client
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if len(devices) == 0:
        print("No phone found! Check USB connection.")
        return None

    print(f"Connected to: {devices[0].serial}")
    return devices[0]

def open_app(device, package_name):
    # Skill: Open an app (e.g., 'com.android.chrome')
    device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
    print(f"Opening {package_name}...")

def take_screenshot(device):
    # Skill: Take a screenshot and save it to Kali
    result = device.screencap()
    with open("phone_screen.png", "wb") as f:
        f.write(result)
    print("Screenshot saved to your Kali folder!")

# --- TEST IT ---
phone = connect_phone()
if phone:
    # Example: Open the Calculator
    open_app(phone, "com.google.android.calculator")

