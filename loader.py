from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from googletrans import Translator

from data import config
from utils.db_api.postgres import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
translator = Translator(service_urls=['translate.googleapis.com'])
__ = translator.translate


def change_lang(phrase):
    langs = ['en', 'ru', 'fr', 'su', 'de', 'ar', 'uk']
    result = []
    for lang in langs:
        result.append(__(phrase, src='ru', dest=lang).text)
    return result
