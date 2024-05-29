import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command

API_TOKEN = '7059847671:AAHKWzoDKOtiCV9EqZMvfUAAoCx9NAhXE6o'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для генерации вариантов ответа
def generate_options():
    options = ["Отличное!", "Хорошое", "Нормальное", "Плохое", "Ужасное"]
    return options

@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Привет! Как твое настроение сегодня?")

@dp.message()
async def process_message(message: Message):
    if message.text.lower() == "как дела?":
        options = generate_options()
        await message.answer("Моё настроение? " + random.choice(options))
    elif message.text.lower() == "спасибо":
        await message.answer("Пожалуйста! Если у вас еще что-то есть, не стесняйтесь спрашивать.")
    elif message.text.lower() == "привет":
        await message.answer("Привет! Как твое настроение сегодня?")     
    else:
        mood_responses = {
            "Хорошое": "Это замечательно!",
            "хорошое": "Это замечательно!",
            "Плохое": "Бывают и такие дни. Надеюсь, всё наладится!",
            "плохое": "Бывают и такие дни. Надеюсь, всё наладится!",
            "Отличное": "Отлично! Рад за вас!",
            "отличное": "Отлично! Рад за вас!",
            "Нормальное": "Хорошо, что не плохо!",
            "нормальное": "Хорошо, что не плохо!",
            "Ужасное": "Мне жаль это слышать. Надеюсь, всё станет лучше.",
            "ужасное": "Мне жаль это слышать. Надеюсь, всё станет лучше.",
            "Иди нахуй": "Сам иди урод ебанный",
            "иди нахуй": "Сам иди урод ебанный"
        }
        response = mood_responses.get(message.text.lower(), "Не могу понять.")
        await message.answer(response)

async def main():
    dp.message.register(send_welcome, Command(commands=["start"]))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
