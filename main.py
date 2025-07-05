import os
import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8088812338:AAEvGsqqJRWUeGO1fDppUBK3uARoCYlAHB8'
ADMIN_ID = 6855997739
CHANNEL_USERNAME = '@y_muhammadyusufxon'
BOT_USERNAME = 'konkurs7m_bot'  # <-- bu yerga botingiz username'ini yozing

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = "users.json"
FAKE_FILE = "fake_users.json"

def load_data():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    else:
        users = {}

    if os.path.exists(FAKE_FILE):
        with open(FAKE_FILE, "r", encoding="utf-8") as f:
            fake_users = json.load(f)
    else:
        fake_users = []

    return users, fake_users

def save_data():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    with open(FAKE_FILE, "w", encoding="utf-8") as f:
        json.dump(fake_users, f, ensure_ascii=False, indent=2)

users, fake_users = load_data()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or "NoUsername"
    args = message.get_args()

    if user_id not in users:
        users[user_id] = {'username': username, 'ref': None, 'points': 0}
        if args.isdigit():
            ref_id = str(args)
            if ref_id != user_id and ref_id in users:
                users[user_id]['ref'] = ref_id
                users[ref_id]['points'] += 10
        save_data()

    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("👥 Do‘st taklif qilish", url=f"https://t.me/{BOT_USERNAME}?start={user_id}")
    )
    await message.answer("Konkurs M Botga xush kelibsiz!\nDo‘stlaringizni taklif qilib ball to‘plang!", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🎯 Ballarim")
async def my_points(message: types.Message):
    user_id = str(message.from_user.id)
    points = users.get(user_id, {}).get('points', 0)
    await message.answer(f"Sizning ballaringiz: {points}")

@dp.message_handler(lambda m: m.text == "🔝 Reyting")
@dp.message_handler(commands=['top'])
async def top_users(message: types.Message):
    combined = [{'name': f"@{v['username']}", 'points': v['points']} for v in users.values()]
    combined += fake_users
    sorted_users = sorted(combined, key=lambda x: x['points'], reverse=True)[:10]
    text = "🏆 TOP 10 ishtirokchi:\n"
    for i, user in enumerate(sorted_users, 1):
        text += f"{i}. {user['name']} – {user['points']} ball\n"
    await message.answer(text)

@dp.message_handler(commands=['add_fake'])
async def add_fake(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.get_args().split('|')
        name = parts[0].strip()
        points = int(parts[1].strip())
        fake_users.append({'name': name, 'points': points})
        save_data()
        await message.answer(f"{name} sun’iy ishtirokchi sifatida qo‘shildi ({points} ball).")
    except:
        await message.answer("Format: /add_fake Ali | 50")

@dp.message_handler(commands=['add_user'])
async def add_user(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.get_args().split()
        uid = str(args[0])
        uname = args[1]
        users[uid] = {'username': uname.replace('@', ''), 'ref': None, 'points': 0}
        save_data()
        await message.answer(f"{uname} bazaga qo‘shildi.")
    except:
        await message.answer("Format: /add_user 123456789 @username")

@dp.message_handler(commands=['add_points'])
async def add_points(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.get_args().split()
        uid = str(args[0])
        pts = int(args[1])
        if uid in users:
            users[uid]['points'] += pts
            save_data()
            await message.answer(f"{pts} ball foydalanuvchiga qo‘shildi.")
        else:
            await message.answer("Foydalanuvchi topilmadi.")
    except:
        await message.answer("Format: /add_points 123456789 50")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
