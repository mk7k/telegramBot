from telethon import TelegramClient
from config import api_id, api_hash, phone
import handlers
from word_game import load_words  # ⬅️ Додай імпорт тут

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    await client.start(phone)
    print("✅ Бот запущено")

    await load_words()  # ⬅️ Завантаження слів перед запуском обробників
    handlers.setup_handlers(client)

    await client.run_until_disconnected()

client.loop.run_until_complete(main())
