import os

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING', 'postgresql://postgres:qwerty@localhost/youtubebot')

WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', None)
CAN_CHANGE_WEBHOOK = os.getenv('CAN_CHANGE_WEBHOOK', 'False')
CAN_CHANGE_WEBHOOK = CAN_CHANGE_WEBHOOK is True or CAN_CHANGE_WEBHOOK.lower() in ['yes', 'y', 'true', 'on', 1]

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_SERVER = os.getenv('TELEGRAM_SERVER', None)
