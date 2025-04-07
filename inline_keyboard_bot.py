from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()

LEXICON = {'but_1': '1',
           'but_2': '2',
           'but_3': '3',
           'but_4': '4',
           'but_5': '5'}

BUTTONS = {'btn_1': '1',
           'btn_2': '2',
           'btn_3': '3',
           'btn_4': '4',
           'btn_5': '5'}

#  Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(3, 'but_1', 'but_2', 'but_3', 'but_4', 'but_5', last_btn='Последняя кнопка')
    await message.answer(
        text='Это инлайн-клавиатура, сформированная функцией ',
        reply_markup=keyboard,
    )


dp.run_polling(bot)
