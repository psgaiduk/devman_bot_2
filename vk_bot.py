from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api as vk
import random
from dotenv import load_dotenv
import os
from work_dialog_flow import detect_intent_texts
import logging
from logging import config

from logger_settings import logger_config

logger = logging.getLogger('app_logger')


def echo(event, vk_api):
    logger.debug(f'Готовимся отвечать пользователю')
    text = detect_intent_texts('careful-gasket-340217', event.user_id, event.text, 'ru-RU')
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

    token_vk = os.environ['VK_TOKEN']

    vk_session = vk.VkApi(token=token_vk)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.debug(f'Это новое сообщение {event.type} {event.to_me}')
            echo(event, vk_api)


if __name__ == "__main__":
    main()
