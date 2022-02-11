import telebot
from work_dialog_flow import detect_intent_texts
from logger_settings import BotHandler
from logging import getLogger, basicConfig, INFO
import os
from dotenv import load_dotenv


logger = getLogger('app_logger')


def repeat_all_messages(message, bot):
    project_id = bot.project_id

    if message.text == '/start':
        logger.debug('Это стартовое сообщение отвечает Здравствуйте')
        text = 'Здравствуйте'
    else:
        logger.debug('Ищем ответ через DialogFlow')
        text, _ = detect_intent_texts(project_id, message.chat.id, message.text, 'ru-RU')
    try:
        bot.send_message(message.chat.id, text)
        logger.debug(f'Отправляю сообщение {text}')
    except Exception as e:
        logger.error(e, exc_info=True)


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    token_telegram = os.environ['TELEGRAM_TOKEN']
    project_id = os.environ['PROJECT_ID']
    logger_token = os.environ['TOKEN_TELEGRAM_LOGGER']
    logger_chat_id = os.environ['CHAT_ID']

    basicConfig(level=INFO, format='{asctime} - {levelname} - {name} - {message}', style='{')
    logger.addHandler(BotHandler(logger_token, logger_chat_id))

    logger.info('Начало работы телеграмм бота Lerning Pashka 2')

    bot = telebot.TeleBot(token=token_telegram)

    bot.project_id = project_id
    bot.register_message_handler(repeat_all_messages, content_types=['text'], pass_bot=True)

    bot.infinity_polling()


if __name__ == '__main__':
    main()
