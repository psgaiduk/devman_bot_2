import os
import telebot
import logging
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logger = logging.getLogger('app_logger')

chat_id = os.environ['CHAT_ID']
token_telegram_logger = os.environ['TOKEN_TELEGRAM_LOGGER']

bot_logger = telebot.TeleBot(token=token_telegram_logger)


class BotHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        message = self.format(record)
        bot_logger.send_message(
            text=f'{message}',
            chat_id=chat_id)


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'bot': {
            '()': BotHandler,
            'level': 'DEBUG',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['bot']
        }
    },
}