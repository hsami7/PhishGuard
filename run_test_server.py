import uvicorn
from app.main import app
import threading
import time
import urllib.request

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")

t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(2)
try:
    urllib.request.urlopen("http://127.0.0.1:8001/")
    print("No error")
except Exception as e:
    print(f"Error caught: {e}")
