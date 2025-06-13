from telethon import events
from config import ALLOWED_CHAT_IDS, EXCLUSIVE_CHAT_IDS
from word_game import process_word_game
import random

# глобальна змінна — буде зберігати client, яку передаємо з main.py
client = None
game_states = {}

def setup_handlers(_client):
    global client
    client = _client

    @client.on(events.NewMessage())
    async def handler(event):
        me = await client.get_me()
        is_saved = event.is_private and event.chat_id == me.id
        is_allowed_chat = event.chat_id in ALLOWED_CHAT_IDS

        if not (is_saved or is_allowed_chat):
            return

        text = event.raw_text.lower()
        user_id = event.sender_id


            # 🧩 Обробка гри в слова
        if await process_word_game(event, user_id, text):
            return  # Якщо це була гра, далі не йдемо


        if event.chat_id in EXCLUSIVE_CHAT_IDS and text == "секрет":
            await event.reply("🔐 Це ексклюзивне повідомлення лише для цього чату!")
            return

        if game_states.get(user_id, {}).get("in_game"):
            if text == "вийти":
                game_states[user_id]["in_game"] = False
                await event.reply("🚪 Вийшов з гри.")
            else:
                try:
                    guess = int(text)
                    secret = game_states[user_id]["number"]
                    if guess == secret:
                        await event.reply(f"🎉 Вгадав! Це було {secret}! Напиши 'гра' щоб ще")
                        game_states[user_id]["in_game"] = False
                    elif guess < secret:
                        await event.reply("🔺 Більше.")
                    else:
                        await event.reply("🔻 Менше.")
                except ValueError:
                    await event.reply("❗ Введи число або 'вийти'.")
            return

        if text == "гра":
            number = random.randint(1, 10)
            game_states[user_id] = {"in_game": True, "number": number}
            await event.reply("🎲 Я загадав число від 1 до 10.Відгадай")
        elif "❤️" in text:
            await event.reply("✅ Сердечко побачив")
        elif "привіт" in text:
            await event.reply("Привіт! Команди: 'гра', 'бот', '❤', '?'")
        elif "?" in text:
            await event.reply("Є питання?")
        elif "бот" in text:
            await event.reply("да я тут!")
