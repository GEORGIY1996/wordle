#!/usr/bin/env python3
import hashlib
import datetime
import sys
import os

GREEN  = "\033[42m\033[30m"
YELLOW = "\033[43m\033[30m"
GRAY   = "\033[100m\033[97m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

WORDS = [
    "абзац", "абрис", "аванс", "агент", "адрес", "актив", "аллея", "альфа",
    "амбар", "анкер", "апорт", "арена", "аргон", "архив", "аспид", "астра",
    "атлас", "атлет", "афиша", "багет", "байка", "балка", "банан", "банда",
    "барак", "барин", "барон", "басня", "бедро", "белок", "берег", "бетон",
    "бизон", "билет", "бирка", "битва", "благо", "бланк", "блеск", "блюдо",
    "борец", "бочка", "браво", "бремя", "броня", "бугор", "буква", "бутон",
    "вагон", "вальс", "варка", "ватка", "вахта", "вдова", "велюр", "венец",
    "верба", "весло", "вилка", "виски", "вихрь", "вклад", "водка", "вожак",
    "вокал", "волна", "волос", "вопль", "ворон", "ворох", "ворот", "газон",
    "галоп", "гамак", "гараж", "гений", "герой", "глава", "глаза", "глина",
    "голос", "гонка", "горец", "горка", "горло", "город", "горох", "гость",
    "грань", "грива", "гроза", "грудь", "грунт", "губка", "гудок", "дебют",
    "диван", "диета", "досуг", "дочка", "дрозд", "дуэль", "дымок", "забор",
    "завод", "загар", "зайка", "залив", "замок", "запах", "зарок", "звено",
    "зефир", "злоба", "знамя", "зубец", "зубок", "игрок", "имидж", "инжир",
    "искра", "исток", "кадет", "казак", "камин", "капот", "карта", "касса",
    "кашне", "кепка", "кивер", "кирка", "кисть", "клоун", "клюка", "книга",
    "кобра", "козёл", "кокон", "колба", "колос", "конус", "копна", "корка",
    "корма", "кость", "кофта", "кочка", "кража", "крест", "крона", "кросс",
    "кроха", "круча", "кузов", "кулак", "купол", "лавка", "ладья", "лазер",
    "ларец", "лента", "лесок", "линза", "лоток", "лунка", "лучок", "лыжня",
    "лютня", "майка", "макет", "марля", "маска", "масло", "масть", "матка",
    "мелок", "место", "метла", "мираж", "могол", "мойка", "молва", "молот",
    "монах", "мотив", "мотор", "мочка", "мушка", "мысль", "набег", "навес",
    "напор", "народ", "насос", "невод", "нефть", "нитка", "норка", "нужда",
    "образ", "обруч", "овраг", "огонь", "олень", "опора", "орден", "охота",
    "пакет", "палач", "палка", "паром", "пасть", "певец", "пекло", "пепел",
    "петля", "пирог", "питон", "плаха", "племя", "плеть", "плита", "плоть",
    "побег", "повод", "погон", "пожар", "позор", "полка", "полог", "порок",
    "порох", "порыв", "посев", "поток", "почва", "права", "приём", "проба",
    "проза", "прыть", "птица", "пудра", "пульт", "пчела", "пышка", "радар",
    "разум", "рамка", "ребро", "рельс", "речка", "рожок", "рокот", "ропот",
    "рубец", "рубин", "рубль", "рулон", "рупор", "ручка", "рыбак", "рычаг",
    "сабля", "салон", "сарай", "связь", "сезон", "склон", "скоба", "скрип",
    "слава", "слива", "смола", "смотр", "собор", "совет", "сойка", "сокол",
    "солод", "сорок", "сосна", "сотня", "спина", "сплав", "среда", "стена",
    "степь", "стиль", "столб", "стопа", "ступа", "судно", "сукно", "сумка",
    "табак", "табор", "тайга", "тайна", "талон", "тариф", "тесто", "титул",
    "товар", "толпа", "томат", "топор", "торец", "тоска", "точка", "трава",
    "тропа", "тулуп", "туман", "тумба", "удача", "узник", "уклон", "улика",
    "умник", "устав", "фасад", "флора", "фляга", "фокус", "форма", "фрукт",
    "халат", "хомяк", "хохот", "хутор", "цапля", "чайка", "чашка", "чудак",
    "чулок", "чурка", "шакал", "шалаш", "шаман", "шапка", "шатёр", "шахта",
    "школа", "шпага", "шпион", "шрифт", "штора", "шуба", "щепка", "щука",
    "экран", "элита", "эпоха", "якорь", "ярлык", "яхта",
]

WORDS = sorted(set(w for w in WORDS if len(w) == 5))

def get_daily_word():
    today = datetime.date.today().isoformat()
    h = int(hashlib.md5(today.encode()).hexdigest(), 16)
    return WORDS[h % len(WORDS)]

def check_guess(guess, answer):
    result = ["gray"] * 5
    answer_chars = list(answer)
    guess_chars = list(guess)

    for i in range(5):
        if guess_chars[i] == answer_chars[i]:
            result[i] = "green"
            answer_chars[i] = None
            guess_chars[i] = None

    for i in range(5):
        if guess_chars[i] is not None and guess_chars[i] in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(guess_chars[i])] = None

    return result

def render_row(letters, colors):
    cells = []
    for letter, color in zip(letters, colors):
        if color == "green":
            cells.append(f"{GREEN} {letter.upper()} {RESET}")
        elif color == "yellow":
            cells.append(f"{YELLOW} {letter.upper()} {RESET}")
        else:
            cells.append(f"{GRAY} {letter.upper()} {RESET}")
    return "  " + " ".join(cells)

def render_empty_row():
    return "  " + " ".join([f"{DIM}[   ]{RESET}"] * 5)

def render_keyboard(used):
    rows = [
        list("йцукенгшщзхъ"),
        list("фывапролджэ"),
        list("ячсмитьбю"),
    ]
    lines = []
    for row in rows:
        line = "  "
        for ch in row:
            color = used.get(ch)
            if color == "green":
                line += f"{GREEN}{ch}{RESET} "
            elif color == "yellow":
                line += f"{YELLOW}{ch}{RESET} "
            elif color == "gray":
                line += f"{GRAY}{ch}{RESET} "
            else:
                line += f"{ch} "
        lines.append(line)
    return "\n".join(lines)

def build_keyboard_state(guesses):
    state = {}
    priority = {"green": 3, "yellow": 2, "gray": 1}
    for letters, colors in guesses:
        for ch, col in zip(letters, colors):
            if priority.get(col, 0) > priority.get(state.get(ch), 0):
                state[ch] = col
    return state

def clear():
    os.system("clear")

def main():
    answer = get_daily_word()
    guesses = []
    max_attempts = 6

    while True:
        clear()
        print(f"\n  {BOLD}ВОРДЛ — угадай слово за 6 попыток{RESET}\n")

        for letters, colors in guesses:
            print(render_row(letters, colors))
        for _ in range(max_attempts - len(guesses)):
            print(render_empty_row())

        print()
        print(render_keyboard(build_keyboard_state(guesses)))
        print()

        won = guesses and all(c == "green" for c in guesses[-1][1])
        if won:
            print(f"  {BOLD}Отлично! Слово угадано: {answer.upper()} 🎉{RESET}\n")
            break
        if len(guesses) == max_attempts:
            print(f"  Увы! Загаданное слово было: {BOLD}{answer.upper()}{RESET}\n")
            break

        try:
            raw = input(f"  Попытка {len(guesses)+1}/{max_attempts} → ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Выход.")
            sys.exit(0)

        if len(raw) != 5:
            input("  Нужно ровно 5 букв. Нажми Enter...")
            continue

        colors = check_guess(list(raw), list(answer))
        guesses.append((list(raw), colors))

if __name__ == "__main__":
    main()
