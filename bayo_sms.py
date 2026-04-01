import subprocess, json

def get_last_sms():
    try:
        res = subprocess.getoutput("termux-sms-list -l 1")
        msg = json.loads(res)[0]
        return f"From {msg['number']}: {msg['body']}"
    except:
        return "No new messages found."

def send_sms(number, text):
    subprocess.run()
    return f"Message sent to {number}."
