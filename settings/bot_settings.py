import os

from aiogram.types import LabeledPrice
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')
SESSION_NAME = 'My_session'
QUERY = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
LIMIT_USER = 200
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')
IMAGE_URL = 'https://www.meme-arsenal.com/memes/02e8c539849dc48732f942548501d987.jpg'
PRICE = LabeledPrice(label='Подписка на 10 дней', amount=30000)