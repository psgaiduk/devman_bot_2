from vk_api import VkApi, longpoll, exceptions
import random
import os
from work_dialog_flow import detect_intent_texts
from logging import config, getLogger
import time
from logger_settings import logger_config

logger = getLogger('app_logger')


def send_auto_answer_to_vk(event, vk_api, project_id):
    logger.debug(f'Готовимся отвечать пользователю')
    text = detect_intent_texts(project_id, event.user_id, event.text, 'ru-RU', 'vk')
    logger.debug(f'Получили ответ от DialogFlow {text}')

    if text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )
        return logger.debug('Отправили сообщение')

    logger.debug('Ответ не нашли, ничего не делаем')


def main():
    config.dictConfig(logger_config)
    logger.info('Начало работы бота ВК Lerning Pashka 2')

    token_vk = os.environ['VK_TOKEN']
    project_id = os.environ['PROJECT_ID']

    vk_session = VkApi(token=token_vk)
    vk_api = vk_session.get_api()
    long_poll = longpoll.VkLongPoll(vk_session)
    for event in long_poll.listen():
        try:
            if event.type == longpoll.VkEventType.MESSAGE_NEW and event.to_me:
                logger.debug(f'Это новое сообщение {event.type} {event.to_me}')
                send_auto_answer_to_vk(event, vk_api, project_id)
        except exceptions.Captcha:
            time.sleep(1)
            logger.warning('Ошибка. Слишком частые запросы.')
        except Exception as e:
            time.sleep(1)
            logger.error(e, exc_info=True)


if __name__ == "__main__":
    main()
