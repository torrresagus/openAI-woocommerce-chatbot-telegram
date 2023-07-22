import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

from open_ai.openAI_chatbot import chat_with_bot

import telebot

telegram_token = os.environ['TELEGRAM_TOKEN']

# Start the bot
bot = telebot.TeleBot(telegram_token)

bot.remove_webhook()

# Respond to the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, os.environ['TELEGRAM_START_MESSAGE'], parse_mode="html")

#To do, collect all messages and save them in the database

@bot.message_handler(content_types=['text'])
def openIA_chat(message):
    response = chat_with_bot(message.text, [])  # Process the message with the chatbot
    bot.send_message(message.chat.id, response, parse_mode="html")

if __name__ == "__main__":
    print("Bot Started")
    bot.infinity_polling()