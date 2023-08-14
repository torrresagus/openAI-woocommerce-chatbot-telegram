from fastapi import APIRouter
from ..models.request_models import ChatRequest
from ..models.response_models import ChatResponse
from ..controllers import chatbot_controller

router = APIRouter()

@router.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request_data: ChatRequest):
    return chatbot_controller.handle_chat_request(request_data)