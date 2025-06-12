from telethon import TelegramClient, events

api_id = 21577857
api_hash = '172804ec1bef86521939e7c654d06cdb'
phone = '+380955036864'

client = TelegramClient('my_session', api_id, api_hash)

# 🔐 Дозволені чати
ALLOWED_CHAT_IDS = [
    #1941150860,  # сістр
    2051027447,   # я тільки другий акк
    #1575299172   # Бодя
]

# Чати з ексклюзивним функціоналом
EXCLUSIVE_CHAT_IDS = [
    2051027447,   # Наприклад, для цього чату буде ексклюзив
    #1941150860   # сістр
]

import random

# Стан гри для кожного користувача
game_states = {}

@client.on(events.NewMessage())
async def handler(event):
    me = await client.get_me()
    is_saved = event.is_private and event.chat_id == me.id
    is_allowed_chat = event.chat_id in ALLOWED_CHAT_IDS

    if not (is_saved or is_allowed_chat):
        return  # Не реагуємо ні на що інше

    text = event.raw_text.lower()
    user_id = event.sender_id

    # Ексклюзивна поведінка для певних чатів
    if event.chat_id in EXCLUSIVE_CHAT_IDS:
        if text == "секрет":
            await event.reply("🔐 Це ексклюзивне повідомлення лише для цього чату!")
            return  # Після ексклюзивної відповіді не йдемо далі

    # 🎮 Якщо користувач зараз у грі
    if game_states.get(user_id, {}).get("in_game"):
        if text == "вийти":
            game_states[user_id]["in_game"] = False
            await event.reply("🚪 Вийшов з гри. До зустрічі!")
        else:
            try:
                guess = int(text)
                secret = game_states[user_id]["number"]
                if guess == secret:
                    await event.reply(f"🎉 Вгадав! Це було число {secret}! Щоб грати ще — напиши 'гра'")
                    game_states[user_id]["in_game"] = False
                elif guess < secret:
                    await event.reply("🔺 Більше.")
                else:
                    await event.reply("🔻 Менше.")
            except ValueError:
                await event.reply("❗ Введи число або 'вийти', щоб завершити гру.")
        return

    # 🎮 Старт гри
    if text == "гра":
        number = random.randint(1, 10)
        game_states[user_id] = {"in_game": True, "number": number}
        await event.reply("🎲 Я загадав число від 1 до 10. Вгадай! Напиши 'вийти', щоб здатися.")
    elif '❤️' in text:
        await event.reply("✅ Сердечко побачив")
    elif 'привіт' in text:
        await event.reply("Привіт! Ця відповіль створена автоматично. Доступні команди: '❤', '?', 'бот', 'гра'")
    elif '?' in text:
        await event.reply("Є питання?")
    elif 'бот' in text:
        await event.reply("да, я тут!")
        
async def show_chat_id():
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(f"{dialog.name} — ID: {dialog.id}")

async def main():
    await client.start(phone)
    print("Бот запущено")
    # await show_chat_id()  # ← використовуй лише для перевірки ID
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
