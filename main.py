from fastapi import FastAPI
import json
import os

app = FastAPI()

MEMORY_FILE = "memory.json"
SECRET_KEY = "Bink1n514819"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

@app.post("/api/memory")
async def add_memory(data: dict):
    if data.get("key") != SECRET_KEY:
        return {"status": "error", "reason": "unauthorized"}

    msg = data.get("message", "")
    if not msg:
        return {"status": "error", "reason": "empty message"}

    memory = load_memory()
    memory.append(msg)
    memory = memory[-5000:]
    save_memory(memory)

    return {"status": "ok", "stored": msg}
