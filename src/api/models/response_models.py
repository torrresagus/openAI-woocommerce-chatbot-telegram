from pydantic import BaseModel

class ChatResponse(BaseModel):
    chat_id: str
    bot_reply: str
