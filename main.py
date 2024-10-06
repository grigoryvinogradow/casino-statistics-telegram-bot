# Data

API_TOKEN = '7753797090:AAHRQZ1EfxkNNwtd_VCslNV8HoxbUi3pLnI'
USERDATA = 'userdata.json'
LOGGING_ENABLED = True

import json, os, time, logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.types import ContentType

def loadJSON(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error with loading JSON: {str(e)}")
        return {}  # Возвращаем пустой словарь в случае ошибки

def saveJSON(data, filename, indent=4):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, sort_keys=True, allow_nan=True, indent=indent)
    except Exception as e:
        print(f"Error with saving JSON: {str(e)}")

# Инициализация users
if not os.path.exists(USERDATA):
    saveJSON({}, USERDATA)  # Создаем пустой JSON файл, если его нет
users = loadJSON(USERDATA)

for user in users:
    print(f"Loaded {user} statistics...")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging_middleware = LoggingMiddleware()
dp.middleware.setup(logging_middleware)

logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class UserRegistrationMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        username = message.from_user.username
        if username and username not in users:
            users[username] = {
                "tries": {
                    "slots": 0,
                    "dice": 0,
                    "dart": 0,
                    "bask": 0,
                    "foot": 0,
                    "bowl": 0
                },
                "wins": {
                    "slots": 0,
                    "dice": 0,
                    "dart": 0,
                    "bask": 0,
                    "foot": 0,
                    "bowl": 0
                },
                "jackpots": {
                    "slots": 0
                },
                "congratulate": True
            }
            saveJSON(users, USERDATA)
            print(f'New user: {username}')

        elif not username:
            await message.bot.send_message(
                message.chat.id,
                f'❗ *ОШИБКА*\nСтатистика недоступна пользователям без указанного username. *Пожалуйста, укажите своё имя пользователя в настройках аккаунта*',
                parse_mode="Markdown",
                message_thread_id=message.message_thread_id
            )

# Добавляем middleware в диспетчер
dp.middleware.setup(UserRegistrationMiddleware())

@dp.message_handler(commands=['casino'])
async def main_menu(message: types.Message):
    username = message.from_user.username

    wins = users.get(username, {}).get("wins", {})
    tries = users.get(username, {}).get("tries", {})
    jackpots = users.get(username, {}).get("jackpots", {}).get("slots", 0)

    slots_wins = wins.get("slots", 0)
    dice_wins = wins.get("dice", 0)
    foot_wins = wins.get("foot", 0)
    bowl_wins = wins.get("bowl", 0)
    bask_wins = wins.get("bask", 0)
    dart_wins = wins.get("dart", 0)

    slots_tries = tries.get("slots", 0)
    dice_tries = tries.get("dice", 0)
    foot_tries = tries.get("foot", 0)
    bowl_tries = tries.get("bowl", 0)
    bask_tries = tries.get("bask", 0)
    dart_tries = tries.get("dart", 0)

    total_tries = slots_tries + dice_tries + foot_tries + bowl_tries + bask_tries + dart_tries
    total_wins = slots_wins + dice_wins + foot_wins + bowl_wins + bask_wins + dart_wins

    await bot.send_message(
        message.chat.id,
        f"""🎰 *ГЛАВНОЕ МЕНЮ*
        Статистика игрока @{username}
        
    ⭐ *Всего джекпотов*: {jackpots}
    ✔ *Всего выигрышей*: {total_wins}
    🏅 *Всего попыток*: {total_tries}

    🎮 *Игры*:
        🎰 *Слоты:* /slot
        🎲 *Кубик:* /dice
        ⚽ *Футбол:* /foot
        🎳 *Боулинг:* /bowl
        🏀 *Баскетбол:* /bask
        🎯 *Дартс:* /dart
        
        *Рейтинг игроков: /rating*
        *Сбросить статистику: /reset*
        *Полная статистика: /stats*
        *Оповещение о выигрыше: /congratulate*""",
        parse_mode="Markdown",
        message_thread_id=message.message_thread_id
    )

@dp.message_handler(commands=['stats'])
async def full_stats(message: types.Message):
    username = message.from_user.username

    wins = users.get(username, {}).get("wins", {})
    tries = users.get(username, {}).get("tries", {})
    jackpots = users.get(username, {}).get("jackpots", {}).get("slots", 0)

    slots_wins = wins.get("slots", 0)
    dice_wins = wins.get("dice", 0)
    foot_wins = wins.get("foot", 0)
    bowl_wins = wins.get("bowl", 0)
    bask_wins = wins.get("bask", 0)
    dart_wins = wins.get("dart", 0)

    slots_tries = tries.get("slots", 0)
    dice_tries = tries.get("dice", 0)
    foot_tries = tries.get("foot", 0)
    bowl_tries = tries.get("bowl", 0)
    bask_tries = tries.get("bask", 0)
    dart_tries = tries.get("dart", 0)

    total_tries = slots_tries + dice_tries + foot_tries + bowl_tries + bask_tries + dart_tries
    total_wins = slots_wins + dice_wins + foot_wins + bowl_wins + bask_wins + dart_wins

    await bot.send_message(
        message.chat.id,
        f"""🎰 *ПОЛНАЯ СТАТИСТИКА*
        Статистика игрока @{username}
        
    ⭐ *Всего джекпотов*: {jackpots}
    ✔ *Всего выигрышей*: {total_wins}
    🏅 *Всего попыток*: {total_tries}

    🎰 *Слоты:*
            Джекпоты: *{jackpots}*
            Выигрыши: *{slots_wins}*
            Попытки: *{slots_tries}*
    🎲 *Кубик:*
            Выигрыши: *{dice_wins}*
            Попытки: *{dice_tries}*
    ⚽ *Футбол:*
            Выигрыши: *{foot_wins}*
            Попытки: *{foot_tries}*
    🎳 *Боулинг:*
            Выигрыши: *{bowl_wins}*
            Попытки: *{bowl_tries}*
    🏀 *Баскетбол:*
            Выигрыши: *{bask_wins}*
            Попытки: *{bask_tries}*
    🎯 *Дартс:*
            Выигрыши: *{dart_wins}*
            Попытки: *{dart_tries}*
        
        *Сбросить статистику: /reset*
        *Вернутся в главное меню: /casino*""",
        parse_mode="Markdown",
        message_thread_id=message.message_thread_id
    )

@dp.message_handler(commands=['reset'])
async def reset_data(message: types.Message):
    users[message.from_user.username] = {
                "tries": {
                    "slots": 0,
                    "dice": 0,
                    "dart": 0,
                    "bask": 0,
                    "foot": 0,
                    "bowl": 0
                },
                "wins": {
                    "slots": 0,
                    "dice": 0,
                    "dart": 0,
                    "bask": 0,
                    "foot": 0,
                    "bowl": 0
                },
                "jackpots": {
                    "slots": 0
                },
                "congratulate": True
            }
    saveJSON(users, USERDATA)
    print(f'{message.from_user.username} reseted his data')

    await bot.send_message(
        message.chat.id,
        f'✅ Статистика пользователя @{message.from_user.username} сброшена',
        parse_mode="Markdown",
        message_thread_id=message.message_thread_id
    )

@dp.message_handler(commands=['congratulate'])
async def congratulate(message: types.Message):
    if users.get(message.from_user.username, {}).get("congratulate", True) == True:
        users[message.from_user.username]["congratulate"] = False
    else:
        users[message.from_user.username]["congratulate"] = True
    saveJSON(users, USERDATA)

    await bot.send_message(
        message.chat.id,
        f'✅ *Настройка сохранена*\nВаша статистика будет по-прежнему записываться, но без оповещения\n_Переключено на {users.get(message.from_user.username, {}).get("congratulate", True)}_',
        parse_mode="Markdown",
        message_thread_id=message.message_thread_id
    )

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    username = message.from_user.username
    await bot.send_message(
        message.chat.id,
        f'🎰 *ПРИВЕТ, @{username}*\nГлавное меню - /casino',
        parse_mode="Markdown",
        message_thread_id=message.message_thread_id
    )

def get_winning_rating():
    """Возвращает рейтинг пользователей по количеству выигрышей."""
    ranking = []
    for username, data in users.items():
        total_wins = sum(data['wins'].values())
        ranking.append((username, total_wins))
    # Сортируем по количеству выигрышей в порядке убывания
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:5]  # Возвращаем только топ-5 пользователей

# Получение рейтинга пользователей по попыткам
def get_attempts_rating():
    """Возвращает рейтинг пользователей по количеству попыток."""
    ranking = []
    for username, data in users.items():
        total_attempts = sum(data['tries'].values())
        ranking.append((username, total_attempts))
    # Сортируем по количеству попыток в порядке убывания
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:5]  # Возвращаем только топ-5 пользователей

# Получение рейтинга пользователей по коэффициенту выигрышей
def get_win_ratio_rating():
    """Возвращает рейтинг пользователей по коэффициенту выигрышей."""
    ranking = []
    for username, data in users.items():
        total_wins = sum(data['wins'].values())
        total_attempts = sum(data['tries'].values())
        win_ratio = total_wins / total_attempts if total_attempts > 0 else 0
        ranking.append((username, win_ratio))
    # Сортируем по коэффициенту выигрышей в порядке убывания
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:5]  # Возвращаем только топ-5 пользователей

# Получение рейтинга пользователей по джекпотам
def get_jackpot_rating():
    """Возвращает рейтинг пользователей по количеству джекпотов."""
    ranking = []
    for username, data in users.items():
        total_jackpots = data['jackpots']['slots']
        ranking.append((username, total_jackpots))
    # Сортируем по количеству джекпотов в порядке убывания
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:5]  # Возвращаем только топ-5 пользователей

def find_user_place(username, sorted_list):
    for index, (name, value) in enumerate(sorted_list, start=1):
        if name == username:
            return index
    return None

@dp.message_handler(commands=['rating'])
async def rating_wins(message: types.Message):
    username = message.from_user.username
    
    win = ""
    attempt = ""
    jackpot = ""
    winrate = ""

    win_rating = sorted(get_winning_rating(), key=lambda x: x[1], reverse=True)
    for index, (name, value) in enumerate(win_rating, start=1):
        win += f"*{index}.* {name} - {value}\n"

    attempts_rating = sorted(get_attempts_rating(), key=lambda x: x[1], reverse=True)
    for index, (name, value) in enumerate(attempts_rating, start=1):
        attempt += f"*{index}.* {name} - {value}\n"

    jackpot_rating = sorted(get_jackpot_rating(), key=lambda x: x[1], reverse=True)
    for index, (name, value) in enumerate(jackpot_rating, start=1):
        jackpot += f"*{index}.* {name} - {value}\n"

    winrate_rating = sorted(get_win_ratio_rating(), key=lambda x: x[1], reverse=True)
    for index, (name, value) in enumerate(winrate_rating, start=1):
        winrate += f"*{index}.* {name} - {round(value, 2)}\n"

    await bot.send_message(
        message.chat.id,
        f'''⭐ *РЕЙТИНГИ ПО СТАТИСТИКЕ*

🎰 *Рейтинг по выигрышу*
    _Ваше место: {find_user_place(username, get_winning_rating())}_
{win}
🎰 *Рейтинг по попыткам*
    _Ваше место: {find_user_place(username, get_attempts_rating())}_
{attempt}
🎰 *Рейтинг по джекпотам*
    _Ваше место: {find_user_place(username, get_jackpot_rating())}_
{jackpot}
🎰 *Рейтинг по винрейту*
    _Ваше место: {find_user_place(username, get_win_ratio_rating())}_
{winrate}
*Вернуться в главное меню - /casino*''',
        parse_mode="Markdown",
        message_thread_id=message.message_thread_id
    )

# Команды для прокрута казино

@dp.message_handler(commands=['dice']) 
async def roll_dice(message: types.Message):
    users[message.from_user.username]["tries"]["dice"] += 1
    data = await bot.send_dice(message.chat.id, emoji='🎲', message_thread_id=message.message_thread_id)

    print(f"Command /dice received from {message.from_user.username} with {data.dice.value} result")

    if data.dice.value == 1:
        users[message.from_user.username]["wins"]["dice"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    
    saveJSON(users, USERDATA)

@dp.message_handler(commands=['dart'])
async def roll_dart(message: types.Message):
    users[message.from_user.username]["tries"]["dart"] += 1
    data = await bot.send_dice(message.chat.id, emoji='🎯', message_thread_id=message.message_thread_id)

    print(f"Command /dart received from {message.from_user.username} with {data.dice.value} result")

    if data.dice.value == 6:
        users[message.from_user.username]["wins"]["dart"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    
    saveJSON(users, USERDATA)

@dp.message_handler(commands=['bask']) 
async def roll_basketball(message: types.Message):
    users[message.from_user.username]["tries"]["bask"] += 1
    data = await bot.send_dice(message.chat.id, emoji='🏀', message_thread_id=message.message_thread_id)

    print(f"Command /bask received from {message.from_user.username} with {data.dice.value} result")

    if data.dice.value == 5 or data.dice.value == 4:
        users[message.from_user.username]["wins"]["bask"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    
    saveJSON(users, USERDATA)

@dp.message_handler(commands=['foot']) 
async def roll_football(message: types.Message):
    users[message.from_user.username]["tries"]["foot"] += 1
    data = await bot.send_dice(message.chat.id, emoji='⚽', message_thread_id=message.message_thread_id)

    print(f"Command /foot received from {message.from_user.username} with {data.dice.value} result")

    if data.dice.value == 3 or data.dice.value == 5:
        users[message.from_user.username]["wins"]["foot"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    
    saveJSON(users, USERDATA)

@dp.message_handler(commands=['bowl']) 
async def roll_bowling(message: types.Message):
    users[message.from_user.username]["tries"]["bowl"] += 1
    data = await bot.send_dice(message.chat.id, emoji='🎳', message_thread_id=message.message_thread_id)

    print(f"Command /bowl received from {message.from_user.username} with {data.dice.value} result")

    if data.dice.value == 6:
        users[message.from_user.username]["wins"]["bowl"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)

    saveJSON(users, USERDATA)

@dp.message_handler(commands=['slot']) 
async def roll_slot(message: types.Message):
    users[message.from_user.username]["tries"]["slots"] += 1
    data = await bot.send_dice(message.chat.id, emoji='🎰', message_thread_id=message.message_thread_id)

    print(f"Command /slot received from {message.from_user.username} with {data.dice.value} result")

    if data.dice.value == 64:
        users[message.from_user.username]["jackpots"]["slots"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Джекпот!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    if data.dice.value == 1 or data.dice.value == 22 or data.dice.value == 43:
        users[message.from_user.username]["wins"]["slots"] += 1
        if users.get(message.from_user.username, {}).get("congratulate", True) == True:
            time.sleep(1)
            await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    
    saveJSON(users, USERDATA)

@dp.message_handler(content_types=ContentType.DICE)
async def handle_dice(message: types.Message):
    value = message.dice.value
    emoji = message.dice.emoji

    if emoji == '🎰':
        users[message.from_user.username]["tries"]["slots"] += 1
        print(f"Slots received from {message.from_user.username} with {value} result")
        #await message.reply(f'Вы запустили слот-машину: {value}')
        if value == 64:
            users[message.from_user.username]["jackpots"]["slots"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Джекпот!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
        if value == 1 or value == 22 or value == 43:
            users[message.from_user.username]["wins"]["slots"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    elif emoji == '🏀':
        #await message.reply(f'Вы бросили мяч в корзину: {value}')
        users[message.from_user.username]["tries"]["bask"] += 1
        print(f"Basketball received from {message.from_user.username} with {value} result")

        if value == 5 or value == 4:
            users[message.from_user.username]["wins"]["bask"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    elif emoji == '🎯':
        #await message.reply(f'Вы бросили дротик: {value}')
        users[message.from_user.username]["tries"]["dart"] += 1
        print(f"Darts received from {message.from_user.username} with {value} result")

        if value == 6:
            users[message.from_user.username]["wins"]["dart"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    elif emoji == '⚽':
        #await message.reply(f'Вы ударили по мячу: {value}')
        users[message.from_user.username]["tries"]["foot"] += 1
        print(f"Football received from {message.from_user.username} with {value} result")

        if value == 3 or value == 5:
            users[message.from_user.username]["wins"]["foot"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    elif emoji == '🎳':
        #await message.reply(f'Вы бросили шар для боулинга: {value}')
        users[message.from_user.username]["tries"]["bowl"] += 1
        print(f"Bowling received from {message.from_user.username} with {value} result")

        if value == 6:
            users[message.from_user.username]["wins"]["bowl"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    elif emoji == '🎲':
        #await message.reply(f'Вы выбиросили кубик: {value}')
        users[message.from_user.username]["tries"]["dice"] += 1
        print(f"Dice cube received from {message.from_user.username} with {value} result")

        if value == 1:
            users[message.from_user.username]["wins"]["dice"] += 1
            if users.get(message.from_user.username, {}).get("congratulate", True) == True:
                time.sleep(1)
                await bot.send_message(message.chat.id, f'🤑 *Выигрыш!* Поздравляем.', parse_mode="Markdown", message_thread_id=message.message_thread_id)
    else:
        await message.reply(f'Неизвестный тип эмодзи: {value}')
    
    saveJSON(users, USERDATA)

original_print = print
def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = ' '.join(map(str, args))
    logging.info(message)
print = custom_print

if __name__ == '__main__':
    print('Bot is starting...')
    executor.start_polling(dp, skip_updates=True)
