import asyncio
import datetime
import logging

from tg_bot import TgBot, register_all_handlers, register_all_filters, kb, Base, DBInteraction
from tg_bot.config import load_config
from data import schools, colleges


config = load_config('bot.ini')
tg_bot = TgBot(config=config, schools=schools, colleges=colleges)

if __name__ == '__main__':
    try:
        asyncio.run(tg_bot.run(register_all_filters=register_all_filters, register_all_handlers=register_all_handlers))
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
