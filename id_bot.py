from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
import aiohttp
import asyncio
from aiogram.client.bot import DefaultBotProperties
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BOT_TOKEN = "7968332774:AAHZi-GKP-QzVzmTau_tUBk1PL6HyfyMJ_I"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("👋 Привіт! Я бот на aiogram 3!")

@dp.message(F.text.lower().contains("привіт"))
async def hello_handler(message: Message):
    await message.answer("Привіт, чемпіоне 😎")

@dp.message(F.text == "/цитата")
async def send_quote(message: types.Message):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get("https://api.quotable.io/random") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    quote = f"“{data['content']}”\n— {data['author']}"
                    await message.answer(quote)
                else:
                    await message.answer("🚫 Не вдалося отримати цитату.")
    except Exception as e:
        await message.answer(f"⚠️ Помилка: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
