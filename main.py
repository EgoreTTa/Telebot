import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ Переменная API_TOKEN не найдена. Проверьте .env или окружение.")

import telebot

bot = telebot.TeleBot(API_TOKEN)

user = {'id':712432196,}

#765932012 admin
#712432196 mtest

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Чем я могу помочь?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if message.from_user.id != 765932012:
		user['id'] = message.from_user.id
		user['mes'] = message
		user['mes.id'] = message.message_id
		user['mes.chat.id'] = message.chat.id
		bot.forward_message(765932012, user.get('id'), user.get('mes.id'))
		bot.send_message(user.get('id'), "Подожди секундочку. :з")
	else:
		bot.send_message(765932012, "Пересылаю юзеру " + str(user.get('id')) + str(user) + " :з")
		bot.reply_to(user.get('mes'), message.text)

bot.infinity_polling()
