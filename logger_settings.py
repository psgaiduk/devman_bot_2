from constants import CHAT_ID_LOGGER, TOKEN_TELEGRAM_LOGGER
import telebot
import logging


logger = logging.getLogger('app_logger')

bot_logger = telebot.TeleBot(token=TOKEN_TELEGRAM_LOGGER)


class BotHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        message = self.format(record)
        bot_logger.send_message(
            text=f'{message}',
            chat_id=CHAT_ID_LOGGER)


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