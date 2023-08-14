from fastapi import FastAPI
from api.routes import chatbot_routes

app = FastAPI()

app.include_router(chatbot_routes.router, tags=["chatbot"])
