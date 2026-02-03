from fastapi import FastAPI
import threading
from monitor import loop

app = FastAPI()

# Start loop monitoring saat service start
@app.on_event("startup")
def start_monitor():
    threading.Thread(target=loop, daemon=True).start()

# Endpoint dummy → buat cek service hidup
@app.get("/")
def root():
    return {"status": "monitor running"}
