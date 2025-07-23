import logging
import random
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout

# <-- TOKENINGIZNI YERGA QO'YING
API_TOKEN = "7475129855:AAFCxNPvQ11ZK0zU-kujOvJbt-4BzTHUjPM"  # xavfsizlik uchun asl tokenni ochiq yozmang!

# Free hisoblar uchun PROXY SOZLAMASI (PythonAnywhere)
PROXY_URL = "http://proxy.server:3128"

# Logging
logging.basicConfig(level=logging.INFO)

# Session (proxy bilan)
timeout = ClientTimeout(total=60)
session = AiohttpSession(proxy=PROXY_URL, timeout=timeout)

bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()


# Guruh filtri
class IsGroup(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ["group", "supergroup"]


@dp.message(IsGroup())
async def reply_with_random_word(message: Message):
    try:
        # Fayl joylashgan joy (shu fayl bilan bir papkada)
        file_path = os.path.join(os.path.dirname(__file__), "sozlar.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            words = [line.strip() for line in file if line.strip()]

        if words:
            random_word = random.choice(words)
            await message.reply(random_word)
        else:
            await message.reply("❗ sozlar.txt bo‘sh!")
    except FileNotFoundError:
        await message.reply("❗ sozlar.txt topilmadi!")


# Botni ishga tushurish
async def main():
    await dp.start_polling(bot)


# Entry point
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
