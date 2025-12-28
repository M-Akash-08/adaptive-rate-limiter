from fastapi import FastAPI
from middleware import RateLimiterMiddleware
import threading
from adaptive_controller import adaptive_controller

app = FastAPI()
app.add_middleware(RateLimiterMiddleware)

@app.on_event("startup")
def start_controller():
    thread = threading.Thread(target=adaptive_controller, daemon=True)
    thread.start()

@app.get("/api/data")
def data():
    return {"message": "Request allowed"}

@app.get("/health")
def health():
    return {"status": "ok"}
