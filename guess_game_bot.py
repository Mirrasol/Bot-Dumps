import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

users = {}

ATTEMPTS = 8


def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Hi! Would you like to play the game \'Guess My Number\'?\n\n'
        'To read the rules and get the list of all available '
        'commands - send /help.'
    )
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {
            'in_game': False,
            'goal_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0,
        }


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'The rules are as follows:\n\n'
        'I make up a number and you need to guess it! '
        f'You have {ATTEMPTS} attempts.\n\n'
        'Available commands:\n'
        '/help - get to the rules and the list of commands,\n'
        '/cancel - quit the game,\n'
        '/stat - check the statistics,\n'
        '/game - start the new game\n\n'
    )
    await message.answer(
        'Wanna play?\n'
        'Send "yes" to start or "no" to wait.'
    )


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await message.answer(
            'Sorry, you need to /start first!'
        )
    else:
        await message.answer(
            f'Total games count: {users[user_id]["total_games"]}\n'
            f'Wins: {users[user_id]["wins"]}'
        )


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    user_id = message.from_user.id
    current_user = users[user_id]
    if current_user['in_game']:
        current_user['in_game'] = False
        await message.answer(
            'You have left the game. If you wish to come back - \n'
            'let me know.'
        )
    else:
        await message.answer(
            'But we are not playing at the moment!\n'
            'Maybe one round?'
        )


@dp.message(F.text.lower().in_(['yes', '"yes"', 'y', 'ye', 'да', 'ага', 'д', '+']))
async def process_starting_game(message: Message):
    user_id = message.from_user.id
    current_user = users[user_id]
    if not current_user['in_game']:
        current_user['in_game'] = True
        current_user['goal_number'] = get_random_number()
        current_user['attempts'] = ATTEMPTS
        await message.answer(
            'Got ya!\n\nI have one number from 1 to 100, '
            'try to guess it!'
        )
    else:
        await message.answer(
            'While in game, I can understand only numbers from 1 to 100 '
            'or commands /cancel and /stat.'
        )


@dp.message(F.text.lower().in_(['no', '"no"', 'nope', 'n']))
async def process_not_starting_game(message: Message):
    user_id = message.from_user.id
    current_user = users[user_id]
    if not current_user['in_game']:
        await message.answer(
            'Too bad :(\n\nShould you change your mind - '
            'let me know!'
        )
    else:
        await message.answer(
            'We\'re in the middle of the game!\n'
            'Please, send me numbers from 1 to 100.'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    user_id = message.from_user.id
    current_user = users[user_id]
    if current_user['in_game']:
        if int(message.text) == current_user['goal_number']:
            current_user['in_game'] = False
            current_user['total_games'] += 1
            current_user['wins'] += 1
            await message.answer(
                'Hooray! You\'ve guessed it!\n\n'
                'Maybe one more round?'
            )
        elif int(message.text) > current_user['goal_number']:
            current_user['attempts'] -= 1
            await message.answer('My number is smaller')
        elif int(message.text) < current_user['goal_number']:
            current_user['attempts'] -= 1
            await message.answer('My number is bigger')

        if current_user['attempts'] == 0:
            current_user['in_game'] = False
            current_user['total_games'] += 1
            await message.answer(
                'Oh no, you are out of turns. '
                'Game\'s over :(\n\nMy number was '
                f'{current_user["goal_number"]}\n\nLet\'s try again?'
            )
    else:
        await message.answer(
            'We are not playing at the moment!\n'
            'Maybe one round?'
        )


@dp.message()
async def process_other_messages(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await message.answer(
            'Sorry, you need to /start first!'
        )
    else:
        current_user = users[user_id]
        if current_user['in_game']:
            await message.answer(
                'We\'re in the middle of the game!\n'
                'Please, send me numbers from 1 to 100.'
            )
        else:
            await message.answer(
                'Sorry, that\'s beyond my capabilities :(\n'
                'Maybe let\'s play a game?'
            )


if __name__ == "__main__":
    dp.run_polling(bot)
