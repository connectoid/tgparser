import logging
from datetime import datetime, timedelta, timezone

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from settings import bot_settings
from bot_menu import menu
from database import orm


logging.basicConfig(
    level=logging.INFO,
    filename = "botlog.log",
    filemode='a',
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

# client = TelegramClient(bot_settings.SESSION_NAME, bot_settings.API_ID, bot_settings.API_HASH)
# client.start()

bot = Bot(token=bot_settings.BOT_TOKEN)
storage = MemoryStorage() 
dp = Dispatcher(bot, storage=storage)

'''Состояния'''

class ChatOpenLink(StatesGroup):
    waiting_link = State()

class ParsingActive(StatesGroup):
    waiting_link = State()
    last_activity = State()

class ParsingPhones(StatesGroup):
    waiting_link = State()

'''Команды'''

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Перезапустить бота'),
        ]
    )

'''Главное меню'''

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    text = f'Привет *{message.from_user.first_name}*!\nВаш ID: {message.from_user.id}\nЯ могу спарсить любой чат\nВыбери необходимое действие👇'
    inline_markup = await menu.main_menu()
    response = orm.add_user(message.from_user.id, message.from_user.username)
    inline_markup = await menu.main_menu()
    username = message.from_user.username
    if response == 1:
        users = orm.get_admins()
        for user in users:
                if message.from_user.username == None:
                    await bot.send_message(user.tg_id, text=f'Пользователь <a href="tg://user?id={message.from_user.id}">@{message.from_user.first_name}</a> присоединился', parse_mode='HTML')
                elif message.from_user.username != None:
                    await bot.send_message(user.tg_id, text=f'Пользователь <a href="tg://user?id={message.from_user.id}">@{username}</a> присоединился', parse_mode='HTML')
                else:
                   await bot.send_message(user.tg_id, text=f'Пользователь <a href="tg://user?id={message.from_user.id}">@{username}</a> присоединился', parse_mode='HTML') 
    await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
    await set_default_commands(dp)

'''Вызов главного меню'''

@dp.callback_query_handler(lambda call: 'main_menu' in call.data)
async def get_main_menu(callback_query: types.CallbackQuery):
    text = f'Привет *{callback_query.from_user.first_name}*!\nВаш ID: {callback_query.from_user.id}\nЯ могу спарсить любой чат\nВыбери необходимое действие👇'
    inline_markup = await menu.main_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Вызов премиум меню'''

@dp.callback_query_handler(lambda call: 'premium_menu' in call.data)
async def get_premium_menu(callback_query: types.CallbackQuery):
    if orm.check_premium(callback_query.from_user.id) == 1:
        text = 'Выберите необходимый вариант из списка'
        inline_markup = await menu.premium_parsing_menu()
        await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        text = 'Данная функция доступна только премиум пользователям'
        await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')

'''Кнопка для открытого парсинга'''

@dp.callback_query_handler(lambda call: 'parsing_open_start' in call.data)
async def parsing_open_start(callback_query: types.CallbackQuery):
    text = 'Отправьте ссылку на ваш чат в формате *t.mе/durоv* или *@durоv*'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await ChatOpenLink.waiting_link.set()

'''Кнопка по дате последнего посещения'''

@dp.callback_query_handler(lambda call: 'parsing_activity' in call.data)
async def parsing_activity_start(callback_query: types.CallbackQuery):
    text = 'Отправьте ссылку на чат'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await ParsingActive.waiting_link.set()

'''Запрос фильтра по активности'''

@dp.message_handler(state=ParsingActive.waiting_link)
async def get_filter_activity(message: types.Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    inline_markup = await menu.last_active_menu()
    text = 'За какой промежуток времени пользователи должны были быть онлайн?'
    await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
    await ParsingActive.last_activity.set()

'''Кнопка моб. телефоны'''

@dp.callback_query_handler(lambda call: 'phones' in call.data)
async def parsing_phones(callback_query: types.CallbackQuery):
    text = 'Отправьте ссылку на чат'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await ParsingPhones.waiting_link.set()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)