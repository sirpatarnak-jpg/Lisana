import os
import json
import asyncio
from fastapi import FastAPI
from discord.ext import commands
import uvicorn

app = FastAPI()

MEMORY_FILE = "memory.json"
SECRET_KEY = "Bink1n514819"

bot = commands.Bot(command_prefix="!")

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

async def start_bot():
    await bot.start(os.getenv("DISCORD_TOKEN"))

async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8080)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        start_api(),
        start_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
