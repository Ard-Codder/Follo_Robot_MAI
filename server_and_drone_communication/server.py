from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Message(BaseModel):
    content: str

messages: List[Message] = []

@app.post("/send_message/")
async def send_message(message: Message):
    messages.append(message)
    return {"status": "success"}

@app.get("/get_messages/")
async def get_messages():
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")
    return messages