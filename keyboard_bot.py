from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

button1 = KeyboardButton(text='Owls')
button2 = KeyboardButton(text='Bell Peppers')

keyboard = ReplyKeyboardMarkup(keyboard=[[button1, button2]])

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Who\'s the most majestic dino descendant?',
        reply_markup=keyboard,
    )


@dp.message(F.text == 'Owls')
async def process_owls_reply(message: Message):
    await message.answer(
        text='Yep, those are beautiful feathered dinos of our time',
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(F.text == 'Bell Peppers')
async def process_peppers_reply(message: Message):
    await message.answer(
        text='Well, if you squint really hard...',
        reply_markup=ReplyKeyboardRemove(),
    )


if __name__ == "__main__":
    dp.run_polling(bot)
