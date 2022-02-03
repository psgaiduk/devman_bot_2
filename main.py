from dotenv import load_dotenv
import telebot
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token_telegram = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token=token_telegram)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == '/start':
        text = 'Здравствуйте'
    else:
        text = message.text
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.infinity_polling()
