import random

WORDS = ["айфон", "робот", "кіт", "літо", "тролейбус", "дощ", "чай", "молоко", "ракета", "вишня"]

user_game_state = {}

def get_hint(word, guess):
    # Формує підказку: правильні букви на своїх позиціях, інші - _
    hint = []
    for w_char, g_char in zip(word, guess):
        if w_char == g_char:
            hint.append(w_char)
        else:
            hint.append('_')
    # Якщо слово вгадане коротше, додаємо _
    if len(guess) < len(word):
        hint.extend(['_'] * (len(word) - len(guess)))
    return ''.join(hint)

async def process_word_game(event, user_id, text):
    state = user_game_state.get(user_id)

    if text == "слова":
        word = random.choice(WORDS)
        user_game_state[user_id] = {"word": word, "tries": 0, "in_game": True}
        await event.reply("🧠 Я загадав українське слово. Вгадай! Напиши 'вихід', щоб здатися.")
        return True

    if text == "вихід" and state and state["in_game"]:
        user_game_state[user_id]["in_game"] = False
        await event.reply("🚪 Ти здався. Може наступного разу?")
        return True

    if state and state["in_game"]:
        state["tries"] += 1
        word = state["word"]
        guess = text

        if guess == word:
            await event.reply(f"🎉 Вгадав! Це було слово «{word}» за {state['tries']} спроб!")
            state["in_game"] = False
        else:
            hint = get_hint(word, guess)
            await event.reply(f"❌ Ні, спробуй ще. Підказка: {hint}")
        return True

    return False
