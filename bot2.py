import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatPermissions, ChatMember
from aiogram.filters import Command, CommandStart
from datetime import timedelta


API_TOKEN = '7447185630:AAERfBsj8oKHACgYMuoecfhlRJkAuIWF2yU'
ADMIN_ID = 1844219820
GROUP_ID = '-4222923592'
INVITE_LINK = 'https://t.me/+vNegPXd_2FthNDgy'
BAN_DURATION = timedelta(seconds=60)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

BANNED_WORDS = ['блять', 'сука', 'нахуй', 'блядота', 'ебливая', 'пидорас']

@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Привет! Вы можете использовать команды /ban и /unban, если вы админ.")

@dp.message(Command('ban'))
async def ban_user(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для использования этой команды.")
        return

    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение пользователя.")
        return

    user_id = message.reply_to_message.from_user.id
    try:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=message.date + BAN_DURATION)
        await message.answer(f"Пользователь {user_id} был забанен на 60 секунд.")

        await bot.send_message(GROUP_ID, f"Пользователь {user_id} был забанен.")

    except Exception as e:
        await message.answer(f"Не удалось забанить пользователя. Ошибка: {e}")

@dp.message(Command('unban'))
async def unban_user(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для использования этой команды.")
        return

    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение пользователя.")
        return

    user_id = message.reply_to_message.from_user.id
    try:
        await bot.unban_chat_member(chat_id=message.chat.id, user_id=user_id, only_if_banned=True)
        await message.answer(f"Пользователь {user_id} был разбанен.")

        await bot.send_message(user_id, f"Вы были разбанены. Вот ссылка на группу: {INVITE_LINK}")

        await bot.send_message(GROUP_ID, f"Пользователь {user_id} был разбанен.")

    except Exception as e:
        await message.answer(f"Не удалось разбанить пользователя. Ошибка: {e}")

@dp.message()
async def check_for_banned_words(message: Message):
    if message.text:  # Check if the message has text
        if any(banned_word in message.text.lower() for banned_word in BANNED_WORDS):
            user_id = message.from_user.id
            try:
                await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=message.date + BAN_DURATION)
                await message.answer(f"Пользователь {user_id} был забанен на 60 секунд потому что плохой(плохая) мальчик(девочка).")

                await bot.send_message(GROUP_ID, f"Пользователь {user_id} был забанен потому что плохой(плохая) мальчик(девочка).")

            except Exception as e:
                await message.answer(f"Не удалось забанить пользователя. Ошибка: {e}")
    else:
        logging.info("Received message without text content.")

@dp.message(Command('mute'))
async def mute_user(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для использования этой команды.")
        return

    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение пользователя.")
        return

    user_id = message.reply_to_message.from_user.id
    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            ),
            until_date=message.date + BAN_DURATION
        )
        await message.answer(f"Пользователь {user_id} был замучен на 7 секунд.")

        await bot.send_message(GROUP_ID, f"Пользователь {user_id} был замучен на 7 секунд.")

    except Exception as e:
        await message.answer(f"Не удалось замутить пользователя. Ошибка: {e}")   
        
async def main():
    dp.message.register(send_welcome, Command(commands=["start"]))
    dp.message.register(ban_user, Command(commands=["ban"]))
    dp.message.register(unban_user, Command(commands=["unban"]))
    dp.message.register(mute_user, Command(commands=["mute"]))
    dp.message.register(check_for_banned_words)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
