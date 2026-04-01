import telebot
import sqlite3
import os

# 1. PEGAR O TOKEN: Mude para o seu token do @BotFather ou use Variável de Ambiente
TOKEN = "SEU_TOKEN_AQUI" 
bot = telebot.TeleBot(TOKEN)

# --- BANCO DE DADOS ---
def iniciar_db():
    conn = sqlite3.connect('memoria.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS memoria 
                      (chave TEXT PRIMARY KEY, valor TEXT)''')
    conn.commit()
    return conn

db = iniciar_db()

# --- LÓGICA DO ROBÔ ---

# Comando /salvar: Ex: /salvar cor favorita: azul
@bot.message_handler(commands=['salvar'])
def salvar(message):
    try:
        # Pega o texto após o comando e divide em Chave : Valor
        conteudo = message.text.replace('/salvar ', '')
        chave, valor = conteudo.split(':')
        
        cursor = db.cursor()
        cursor.execute("INSERT OR REPLACE INTO memoria (chave, valor) VALUES (?, ?)", 
                       (chave.strip().lower(), valor.strip()))
        db.commit()
        
        bot.reply_to(message, f"✅ Entendi! Guardei que '{chave.strip()}' é '{valor.strip()}'.")
    except:
        bot.reply_to(message, "⚠️ Use o formato: /salvar termo: descrição")

# Responder a perguntas (Qualquer mensagem que não seja comando)
@bot.message_handler(func=lambda message: True)
def responder(message):
    pergunta = message.text.lower().strip()
    
    cursor = db.cursor()
    cursor.execute("SELECT valor FROM memoria WHERE chave = ?", (pergunta,))
    resultado = cursor.fetchone()
    
    if resultado:
        bot.reply_to(message, f"🤖 Eu sei isso: {resultado[0]}")
    else:
        bot.reply_to(message, "🤔 Ainda não aprendi sobre isso. Use /salvar para me ensinar!")

# Iniciar o Robô
print("Robô ligado no Telegram...")
bot.infinity_polling()
