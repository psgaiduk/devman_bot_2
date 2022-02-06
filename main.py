from dotenv import load_dotenv
import telebot
import os
from work_dialog_flow import detect_intent_texts
from logger_settings import logger_config
import logging
from logging import config

logger = logging.getLogger('app_logger')


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    logging.config.dictConfig(logger_config)

    token_telegram = os.environ['TELEGRAM_TOKEN']

    logger.info('Начало работы телеграмм бота Lerning Pashka 2')

    bot = telebot.TeleBot(token=token_telegram)

    @bot.message_handler(content_types=["text"])
    def repeat_all_messages(message):
        if message.text == '/start':
            logger.debug('Это стартовое сообщение отвечает Здравствуйте')
            text = 'Здравствуйте'
        else:
            logger.debug('Ищем ответ через DialogFlow')
            text = detect_intent_texts('careful-gasket-340217', message.chat.id, message.text, 'ru-RU')
        if text:
            bot.send_message(message.chat.id, text)
            logger.debug(f'Отправляю сообщение {text}')
        else:
            logger.debug('DialogFlow не нашёл ответа, ничего не делаем')

    bot.infinity_polling()


if __name__ == '__main__':
    main()
