from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/support', description='Поддержка'),
        BotCommand(command='/contacts', description='Другие способы связи'),
        BotCommand(command='/payments', description='Платежи'),
    ]
    await bot.set_my_commands(main_menu_commands)

# Регистрируем в диспетчере ф., которая выполнится при старте бота.
# Или добавляем ф. в событийный цикл через aiogram вместо asyncio.
dp.startup.register(set_main_menu)
dp.run_polling(bot)
