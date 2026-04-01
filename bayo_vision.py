import subprocess, os

def take_photo():
    # Saves a photo from your back camera
    photo_path = "vision_temp.jpg"
    try:
        print("[!] Activating Camera...")
        subprocess.run(["termux-camera-photo", "-c", "0", photo_path], check=True)
        return photo_path
    except:
        return None

def scan_text(image_path):
    # Uses Tesseract to turn the image into text
    try:
        print("[!] Running OCR Analysis...")
        subprocess.run(["tesseract", image_path, "out"], capture_output=True)
        with open("out.txt", "r") as f:
            text = f.read().strip()
        return text if text else "I see the image, but I can't read any text on it, Boss."
    except:
        return "Vision error: OCR failed."

def see():
    path = take_photo()
    if path:
        result = scan_text(path)
        os.remove(path) # Clean up
        if os.path.exists("out.txt"): os.remove("out.txt")
        return result
    return "I can't access the camera, Boss."
