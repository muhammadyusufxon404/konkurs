# import logging
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# # Configuration
# API_TOKEN = '8088812338:AAEvGsqqJRWUeGO1fDppUBK3uARoCYlAHB8'  # Bot token from @BotFather
# ADMIN_ID = 6855997739  # Admin Telegram user ID
# CHANNEL_USERNAME = '@y_muhammadyusufxon'  # Your channel
# BOT_USERNAME = '@konkurs7m_bot'  # Replace with your bot's actual username

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)

# # Data storage
# users = {}  # user_id: {'username': str, 'ref': int or None, 'points': int}
# fake_users = []  # [{'name': str, 'points': int}]

# # Check if user is subscribed to the channel
# async def check_subscription(user_id: int) -> bool:
#     try:
#         member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
#         return member.status in ['member', 'administrator', 'creator']
#     except Exception as e:
#         logging.error(f"Subscription check failed for user {user_id}: {e}")
#         return False

# # Start command handler
# @dp.message_handler(commands=['start'])
# async def start_cmd(message: types.Message):
#     user_id = message.from_user.id
#     username = message.from_user.username or "NoUsername"
#     args = message.get_args()

#     # Check subscription
#     if not await check_subscription(user_id):
#         kb = InlineKeyboardMarkup().add(
#             InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
#         )
#         await message.answer(
#             f"Iltimos, avval kanalga obuna bo‘ling: {CHANNEL_USERNAME}",
#             reply_markup=kb
#         )
#         return

#     # Register user if not already in database
#     if user_id not in users:
#         users[user_id] = {'username': username, 'ref': None, 'points': 0}
#         if args.isdigit():
#             ref_id = int(args)
#             if ref_id != user_id and ref_id in users:
#                 users[user_id]['ref'] = ref_id
#                 users[ref_id]['points'] += 10
#                 try:
#                     await bot.send_message(ref_id, "Siz yangi do‘st taklif qildingiz! +10 ball")
#                 except Exception as e:
#                     logging.error(f"Failed to notify referrer {ref_id}: {e}")

#     # Welcome message with referral link
#     kb = InlineKeyboardMarkup().add(
#         InlineKeyboardButton("👥 Do‘st taklif qilish", url=f"https://t.me/{BOT_USERNAME[1:]}?start={user_id}")
#     )
#     await message.answer(
#         "Konkurs M Botga xush kelibsiz!\nDo‘stlaringizni taklif qilib ball to‘plang!",
#         reply_markup=kb
#     )

# # Show user's points
# @dp.message_handler(lambda m: m.text == "🎯 Ballarim")
# async def my_points(message: types.Message):
#     user_id = message.from_user.id
#     points = users.get(user_id, {}).get('points', 0)
#     await message.answer(f"Sizning ballaringiz: {points}")

# # Show top 10 users
# @dp.message_handler(lambda m: m.text == "🔝 Reyting")
# @dp.message_handler(commands=['top'])
# async def top_users(message: types.Message):
#     combined = [{'name': f"@{v['username']}", 'points': v['points']} for v in users.values()]
#     combined += fake_users
#     sorted_users = sorted(combined, key=lambda x: x['points'], reverse=True)[:10]
#     text = "🏆 TOP 10 ishtirokchi:\n"
#     for i, user in enumerate(sorted_users, 1):
#         text += f"{i}. {user['name']} – {user['points']} ball\n"
#     await message.answer(text)

# # Admin command: Add fake user
# @dp.message_handler(commands=['add_fake'])
# async def add_fake(message: types.Message):
#     if message.from_user.id != ADMIN_ID:
#         await message.answer("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
#         return
#     try:
#         parts = message.get_args().split('|', 1)
#         name = parts[0].strip()
#         points = int(parts[1].strip())
#         fake_users.append({'name': name, 'points': points})
#         await message.answer(f"{name} sun’iy ishtirokchi sifatida qo‘shildi ({points} ball).")
#     except (IndexError, ValueError):
#         await message.answer("Format: /add_fake Ali | 50")

# # Admin command: Add real user
# @dp.message_handler(commands=['add_user'])
# async def add_user(message: types.Message):
#     if message.from_user.id != ADMIN_ID:
#         await message.answer("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
#         return
#     try:
#         args = message.get_args().split(maxsplit=1)
#         uid = int(args[0])
#         uname = args[1].strip()
#         users[uid] = {'username': uname.replace('@', ''), 'ref': None, 'points': 0}
#         await message.answer(f"{uname} bazaga qo‘shildi.")
#     except (IndexError, ValueError):
#         await message.answer("Format: /add_user 123456789 @username")

# # Admin command: Add points to user
# @dp.message_handler(commands=['add_points'])
# async def add_points(message: types.Message):
#     if message.from_user.id != ADMIN_ID:
#         await message.answer("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
#         return
#     try:
#         args = message.get_args().split(maxsplit=1)
#         uid = int(args[0])
#         pts = int(args[1])
#         if uid in users:
#             users[uid]['points'] += pts
#             await message.answer(f"{pts} ball foydalanuvchiga qo‘shildi.")
#             try:
#                 await bot.send_message(uid, f"Sizga {pts} ball qo‘shildi!")
#             except Exception as e:
#                 logging.error(f"Failed to notify user {uid}: {e}")
#         else:
#             await message.answer("Foydalanuvchi topilmadi.")
#     except (IndexError, ValueError):
#         await message.answer("Format: /add_points 123456789 50")

# # Main execution
# if __name__ == '__main__':
#     try:
#         executor.start_polling(dp, skip_updates=True)
#     except Exception as e:
#         logging.error(f"Bot polling failed: {e}")

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8088812338:AAEvGsqqJRWUeGO1fDppUBK3uARoCYlAHB8'
ADMIN_ID = 6855997739
CHANNEL_USERNAME = '@y_muhammadyusufxon'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = {}  # user_id: {'username': ..., 'ref': ..., 'points': ...}
fake_users = []  # [{'name': ..., 'points': ...}]

def check_subscription(user_id):
    return True

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    args = message.get_args()

    if not check_subscription(user_id):
        await message.answer(f"Iltimos, avval kanalga obuna bo‘ling:\n{CHANNEL_USERNAME}")
        return

    if user_id not in users:
        users[user_id] = {'username': username, 'ref': None, 'points': 0}
        if args.isdigit():
            ref_id = int(args)
            if ref_id != user_id and ref_id in users:
                users[user_id]['ref'] = ref_id
                users[ref_id]['points'] += 10

    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("👥 Do‘st taklif qilish", url=f"https://t.me/YOUR_BOT_USERNAME?start={user_id}")
    )
    await message.answer("Konkurs M Botga xush kelibsiz!\nDo‘stlaringizni taklif qilib ball to‘plang!", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🎯 Ballarim")
async def my_points(message: types.Message):
    user_id = message.from_user.id
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
        await message.answer(f"{name} sun’iy ishtirokchi sifatida qo‘shildi ({points} ball).")
    except:
        await message.answer("Format: /add_fake Ali | 50")

@dp.message_handler(commands=['add_user'])
async def add_user(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.get_args().split()
        uid = int(args[0])
        uname = args[1]
        users[uid] = {'username': uname.replace('@', ''), 'ref': None, 'points': 0}
        await message.answer(f"{uname} bazaga qo‘shildi.")
    except:
        await message.answer("Format: /add_user 123456789 @username")

@dp.message_handler(commands=['add_points'])
async def add_points(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.get_args().split()
        uid = int(args[0])
        pts = int(args[1])
        if uid in users:
            users[uid]['points'] += pts
            await message.answer(f"{pts} ball foydalanuvchiga qo‘shildi.")
        else:
            await message.answer("Foydalanuvchi topilmadi.")
    except:
        await message.answer("Format: /add_points 123456789 50")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
