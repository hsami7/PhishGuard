import uvicorn
from app.main import app
import threading
import time
import urllib.request
import json

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="debug")

t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(2)

data = json.dumps({"username": "test1", "email": "test1@test.com", "password": "pwd"}).encode("utf-8")
req = urllib.request.Request("http://127.0.0.1:8002/auth/register", data=data, headers={'Content-Type': 'application/json'})

try:
    urllib.request.urlopen(req)
    print("No error")
except Exception as e:
    print(f"Error caught: {e}")
