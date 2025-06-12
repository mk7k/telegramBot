from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F

import asyncio
from aiogram.client.bot import DefaultBotProperties

BOT_TOKEN = "7968332774:AAHZi-GKP-QzVzmTau_tUBk1PL6HyfyMJ_I"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("👋 Привіт! Я бот на aiogram 3!")

@dp.message(F.text.lower().contains("привіт"))
async def hello_handler(message: Message):
    await message.answer("Привіт, чемпіоне 😎")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
