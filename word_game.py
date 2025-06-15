import random

# Завантажені слова з файлу
WORDS = []

# Ігровий стан кожного користувача
user_game_state = {}

async def load_words():
    global WORDS
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            text = f.read()
            # Розділення по пробілах, перенесеннях рядків, табах
            raw_words = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            WORDS = [w.strip().lower() for w in raw_words.split() if w.strip()]
        print(f"✅ Завантажено {len(WORDS)} слів з локального файлу.")
    except Exception as e:
        print(f"❌ Не вдалося завантажити слова: {e}")

# Створення підказки на основі останньої спроби
def get_progress_hint(word, guesses):
    last_guess = guesses[-1]
    hint = []

    for i in range(len(last_guess)):
        if i < len(word):
            if last_guess[i] == word[i]:
                hint.append(f"🔵{last_guess[i]}")  # правильна літера на правильному місці
            elif last_guess[i] in word:
                hint.append(f"🟡{last_guess[i]}")  # літера є, але не там
            else:
                hint.append(f"❌{last_guess[i]}")  # літери немає взагалі
        else:
            hint.append(f"❌{last_guess[i]}")  # зайві символи
    return ' '.join(hint)

# Обробка гри
async def process_word_game(event, user_id, text):
    state = user_game_state.get(user_id)

    if text == "слова":
        word = random.choice(WORDS)
        user_game_state[user_id] = {
            "word": word,
            "tries": 0,
            "in_game": True,
            "guesses": []
        }
        print(f"[DEBUG] Загадане слово: {word}")  # для тебе в консоль
        await event.reply(f"🧠 Я загадав слово з {len(word)} букв. Пиши 'вихід', щоб здатися.")
        return True

    if text == "вихід" and state and state["in_game"]:
        state["in_game"] = False
        await event.reply(f"🚪 Ти здався. Слово було: «{state['word']}». Напиши 'слова', щоб ще.")
        return True

    if state and state["in_game"]:
        word = state["word"]
        guess = text.strip().lower()
        state["tries"] += 1
        state["guesses"].append(guess)

        if guess == word:
            state["in_game"] = False
            await event.reply(f"🎉 Вгадав! Слово було «{word}». {state['tries']} спроб.")
        else:
            hint = get_progress_hint(word, state["guesses"])
            await event.reply(f"❌ Ні, спробуй ще. Підказка: {hint}")
        return True

    return False
