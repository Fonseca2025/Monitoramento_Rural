import os
import telebot
import google.generativeai as genai

# Configurações (Use variáveis de ambiente por segurança no GitHub)
TELEGRAM_TOKEN = os.getenv("8551592126:AAHGVr812nfEm2ipuH-CWlIt0B0rIE4nMlk")
GEMINI_API_KEY = os.getenv("AIzaSyDYF90YUXyCaEjlnh1skBMap8mWM8uj62Q")

# Inicializar APIs
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Aqui carregamos o texto do edital. 
# DICA: Salve o texto do OCR que você me mandou em um arquivo chamado 'edital.txt'
def carregar_edital():
    with open("edital.txt", "r", encoding="utf-8") as f:
        return f.read()

CONTEUDO_EDITAL = carregar_edital()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Sou o assistente do Edital 199/2025 (Montes Claros). O que você deseja saber sobre a licitação de videomonitoramento?")

@bot.message_handler(func=lambda message: True)
def responder_pergunta(message):
    pergunta = message.text
    
    prompt = f"""
    Você é um especialista em licitações. Com base no conteúdo do edital abaixo, responda à pergunta do usuário de forma clara e objetiva.
    Se a informação não estiver no edital, diga que não encontrou.
    
    EDTAL:
    {CONTEUDO_EDITAL[:30000]} # Limitando caracteres para performance
    
    PERGUNTA: {pergunta}
    """
    
    try:
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Erro ao processar. Tente novamente mais tarde.")
        print(e)

print("Bot rodando...")
bot.infinity_polling()
