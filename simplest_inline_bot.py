from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

url_button1 = InlineKeyboardButton(
    text='Курс "Телеграм-боты на Python и AIOgram"',
    url='https://stepik.org/120924',
)
url_button2 = InlineKeyboardButton(
    text='Документация Telegram Bot API',
    url='https://core.telegram.org/bots/api',
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[url_button1], [url_button2]]
)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Inline buttons with url parameter',
        reply_markup=keyboard,
    )


if __name__== "__main__":
    dp.run_polling(bot)
