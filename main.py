from dotenv import load_dotenv
import telebot
import os
from google.cloud import dialogflow


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token_telegram = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token=token_telegram)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == '/start':
        text = 'Здравствуйте'
    else:
        text = detect_intent_texts('careful-gasket-340217', message.chat.id, message.text, 'ru-RU')
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.infinity_polling()
