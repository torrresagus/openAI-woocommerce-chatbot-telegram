from open_ai.openAI_chatbot import chat_with_bot

def handle_chat_request(data):
    response_message = chat_with_bot(data.user_message, data.chat_id)
    return {
        "chat_id": data.chat_id,
        "bot_reply": response_message
    }