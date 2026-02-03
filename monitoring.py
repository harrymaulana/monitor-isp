import requests
import os
import json
from datetime import datetime

# ===== ENV VAR =====
UPTIMEROBOT_API_KEY = os.getenv("UPTIMEROBOT_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STATUS_FILE = "last_status.json"

# ===== Ambil monitor dari UptimeRobot =====
def get_monitors():
    r = requests.post(
        "https://api.uptimerobot.com/v2/getMonitors",
        data={"api_key": UPTIMEROBOT_API_KEY, "format": "json"},
        timeout=10
    )
    return r.json()["monitors"]

# ===== Kirim Telegram =====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

# ===== Load / save status =====
def load_status():
    try:
        with open(STATUS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

# ===== Main =====
def main():
    last_status = load_status()
    current_status = {}
    monitors = get_monitors()

    for m in monitors:
        name = m["friendly_name"]
        status = "UP" if m["status"] == 2 else "DOWN"
        current_status[name] = status

        if last_status.get(name) != status:
            emoji = "🔴" if status == "DOWN" else "🟢"
            waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            send_telegram(f"{emoji} {name}\nStatus: {status}\nWaktu: {waktu}")

    save_status(current_status)

if __name__ == "__main__":
    main()
