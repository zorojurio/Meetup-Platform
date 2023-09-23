import os

from dotenv import load_dotenv

load_dotenv()
EVENT_TRIBE_TOKEN = os.environ.get('EVENT_TRIBE_TOKEN')
EVENT_TRIBE_GET_EVENT_API = os.environ.get('EVENT_TRIBE_GET_EVENT_API')
EVENT_TRIBE_GET_EXTRA = os.environ.get('EVENT_TRIBE_GET_EXTRA')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
