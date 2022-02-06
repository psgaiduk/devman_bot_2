from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api as vk
from vk_api.exceptions import Captcha
import random
from dotenv import load_dotenv
import os
from work_dialog_flow import detect_intent_texts
import logging
from logging import config
import time
from logger_settings import logger_config
from constants import TOKEN_VK, PROJECT_ID

logger = logging.getLogger('app_logger')


def echo(event, vk_api):
    logger.debug(f'Готовимся отвечать пользователю')
    text = detect_intent_texts(PROJECT_ID, event.user_id, event.text, 'ru-RU')
    logger.debug(f'Получили ответ от DialogFlow {text}')

    if text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )
        logger.debug('Отправили сообщение')
    else:
        logger.debug('Ответ не нашли, ничего не делаем')


def main():
    logging.config.dictConfig(logger_config)
    logger.info('Начало работы бота ВК Lerning Pashka 2')
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    vk_session = vk.VkApi(token=TOKEN_VK)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                logger.debug(f'Это новое сообщение {event.type} {event.to_me}')
                echo(event, vk_api)
        except Captcha:
            time.sleep(1)
            logger.warning('Ошибка. Слишком частые запросы.')
        except Exception as e:
            time.sleep(1)
            logger.exception(f'Произошла ошибка.\n{e}')


if __name__ == "__main__":
    main()
