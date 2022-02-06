from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


CHAT_ID_LOGGER = os.environ['CHAT_ID']
TOKEN_TELEGRAM_LOGGER = os.environ['TOKEN_TELEGRAM_LOGGER']
TOKEN_TELEGRAM = os.environ['TELEGRAM_TOKEN']
PROJECT_ID = os.environ['PROJECT_ID']
TOKEN_VK = os.environ['VK_TOKEN']
