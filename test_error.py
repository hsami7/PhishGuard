from fastapi.testclient import TestClient
from app.main import app
try:
    client = TestClient(app)
    client.get("/")
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
