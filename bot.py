import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Olá! O robô está funcionando no Render!")

# Rota para o Render não dar erro de porta e para o Webhook
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    # Substitua pela sua URL do Render depois de criar o serviço
    bot.set_webhook(url='https://seu-projeto.onrender.com/' + TOKEN)
    return "Bot de pé!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
