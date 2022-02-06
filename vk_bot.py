from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api as vk
import random
from dotenv import load_dotenv
import os
from work_dialog_flow import detect_intent_texts

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token_vk = os.environ['VK_TOKEN']


def echo(event, vk_api):
    text = detect_intent_texts('careful-gasket-340217', event.user_id, event.text, 'ru-RU')

    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=token_vk)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
