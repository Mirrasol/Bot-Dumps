from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '7274875670:AAHD2swgWpB308UVqg3xEht_-yFBgnYgBy4'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    """Processing the command /start."""
    await message.answer("Hi there!\nI'm Echo-bot!\nTell me something?")


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    """Processing the command /help."""
    await message.answer("Write something here and I will echo it to you!")


@dp.message(F.voice)
async def process_voice_message(message: Message):
    await message.answer(text='Got the message! Such a nice voice you have!')


@dp.message()
async def send_echo(message: Message):
    """Processing user messages."""
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Message type is not supported, sorry :(')


if __name__ == "__main__":
    dp.run_polling(bot)
