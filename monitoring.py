import requests
import json
import os
import time
from datetime import datetime

# ======= CONFIG =======
UPTIMEROBOT_API_KEY = os.getenv("UPTIMEROBOT_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STATUS_FILE = "last_status.json"  # simpan status terakhir supaya ga spam
# =====================

# Ambil status monitor dari UptimeRobot
def get_monitors():
    r = requests.post(
        "https://api.uptimerobot.com/v2/getMonitors",
        data={
            "api_key": UPTIMEROBOT_API_KEY,
            "format": "json"
        },
        timeout=10
    )
    return r.json()["monitors"]

# Kirim notif ke Telegram
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=10
    )

# Load status lama (anti spam)
def load_status():
    if not os.path.exists(STATUS_FILE):
        return {}
    with open(STATUS_FILE) as f:
        return json.load(f)

# Simpan status terbaru
def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

# Loop utama
def loop():
    last_status = load_status()

    while True:
        try:
            monitors = get_monitors()
            current_status = {}

            for m in monitors:
                name = m["friendly_name"]
                status = "UP" if m["status"] == 2 else "DOWN"
                current_status[name] = status

                # Cek perubahan status → kirim notif
                if last_status.get(name) != status:
                    emoji = "🔴" if status == "DOWN" else "🟢"
                    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    send_telegram(
                        f"{emoji} {name}\nStatus: {status}\nWaktu: {waktu}"
                    )

            save_status(current_status)
            last_status = current_status

        except Exception as e:
            send_telegram(f"⚠️ Error monitor: {e}")

        time.sleep(60)  # cek tiap 60 detik
