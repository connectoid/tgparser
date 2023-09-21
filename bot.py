import logging
import glob
import os
import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from telethon.errors.rpcerrorlist import UsernameInvalidError, ChatAdminRequiredError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from pyrogram.errors.exceptions.bad_request_400 import InviteHashExpired

from settings import bot_settings
from bot_menu import menu
from database import orm
from request_report import request, create_report
from lexicon.lexicon_ru import *
USER_PARSE_DELAY = 1

logging.basicConfig(
    level=logging.ERROR,
    filename = "botlog.log",
    filemode='a',
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

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

class ChatPrivateLink(StatesGroup):
    waiting_link = State()

class ParsingMessages(StatesGroup):
    waiting_link = State()
    count = State()

class Mailing(StatesGroup):
    text = State()
    entity = State()

class Get_id_premium(StatesGroup):
    user_id = State()

class Get_id_admin(StatesGroup):
    user_id = State()

'''Команды'''

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Главное меню'),
        ]
    )

'''Валидация ссылки на приватный чат'''

async def check_private_link(link):
    try:
        chat = await request.app.get_chat(link)
        try:
            count = await request.app.get_chat_members_count(chat.id)
            logging.info(f'Сссылка {link} на приватный чат прошла валидацию')
            return True
        except ValueError as e:
            logging.info(f'Сссылка {link} на приватный чат НЕ прошла валидацию - {e}')
            return False
        except:
            logging.info(f'Сссылка {link} на приватный чат НЕ прошла валидацию (неизвестная ошибка)')
            return False
    except:
        logging.info(f'Сссылка {link} на приватный чат НЕ прошла валидацию')
        return False

'''Валидация ссылок'''

async def trim_link(link: str):
    print(link)
    if link.startswith('https://t.me/'):
        link = link.replace('https://t.me/', '@')
    print(link)
    return link

async def check_link(link):
    try:
        channel = await request.client.get_entity(link)
        try:
            participants = await request.client(GetParticipantsRequest(channel, ChannelParticipantsSearch('a'), 0, bot_settings.LIMIT_USER, hash=0))
            logging.info(f'Сссылка {link} прошла валидацию')
            return True
        except (ChatAdminRequiredError, TypeError):
            logging.info(f'Сссылка {link} не прошла валидацию (возможно сслыка на канал вместо чата)')
            return False
    except InviteHashExpired as e:
        logging.info(f'Сссылка {link} на подключение к приватному чату просрочена - {e}')
        return False
    except UsernameInvalidError as e:
        logging.info(f'Сссылка {link} не прошла валидацию - {e}')
        return False
    except ValueError as e:
        logging.info(f'Сссылка {link} не прошла валидацию - {e}')
        return False
    except ChatAdminRequiredError as e:
        logging.info(f'Сссылка {link} не прошла валидацию - {e}')
        return False
    except:
        logging.info(f'Сссылка {link} не прошла валидацию (не опознанная ошибка)')
        return False

'''Главное меню'''

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    text = HELLO_MESSAGE
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

''' Кнопка назад '''

@dp.callback_query_handler(state=ChatOpenLink.waiting_link)
@dp.callback_query_handler(state=ParsingActive.waiting_link)
@dp.callback_query_handler(state=ParsingPhones.waiting_link)
@dp.callback_query_handler(state=ChatPrivateLink.waiting_link)
@dp.callback_query_handler(state=ParsingMessages.waiting_link)
@dp.callback_query_handler(lambda call: 'back_to_main_menu' in call.data)
async def get_open_report(callback_query: types.CallbackQuery, state: FSMContext):
    text = HELLO_MESSAGE
    inline_markup = await menu.main_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    await state.finish()

'''Вызов главного меню'''

@dp.callback_query_handler(lambda call: 'main_menu' in call.data)
async def get_main_menu(callback_query: types.CallbackQuery):
    text = HELLO_MESSAGE
    inline_markup = await menu.main_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Вызов премиум меню'''

@dp.callback_query_handler(lambda call: 'premium_menu' in call.data)
async def get_premium_menu(callback_query: types.CallbackQuery):
    if orm.check_premium(callback_query.from_user.id) == 1:
        text = PREMIUM_CHOICE_MESSAGE
        inline_markup = await menu.premium_parsing_menu()
        await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        text = PREMIUM_NEED_MESSAGE
        await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')

'''Кнопка для открытого парсинга'''

@dp.callback_query_handler(lambda call: 'parsing_open_start' in call.data)
async def parsing_open_start(callback_query: types.CallbackQuery):
    text = WAITING_LINK_MESSAGE
    inline_markup = await menu.back_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    await ChatOpenLink.waiting_link.set()

'''Кнопка по дате последнего посещения'''

@dp.callback_query_handler(lambda call: 'parsing_activity' in call.data)
async def parsing_activity_start(callback_query: types.CallbackQuery):
    text = WAITING_LINK_MESSAGE
    inline_markup = await menu.back_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    await ParsingActive.waiting_link.set()

'''Запрос фильтра по активности'''

@dp.message_handler(state=ParsingActive.waiting_link)
async def get_filter_activity(message: types.Message, state: FSMContext):
    if await check_link(message.text):
        await state.update_data(waiting_link=message.text)
        inline_markup = await menu.last_active_menu()
        text = ACTIVITY_PERIOD_MESSAGE
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
        await ParsingActive.last_activity.set()
    else:
        text = WRONG_CHAT_MESSAGE
        inline_markup = await menu.back_menu()
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Кнопка моб. телефоны'''

@dp.callback_query_handler(lambda call: 'phones' in call.data)
async def parsing_phones(callback_query: types.CallbackQuery):
    text = WAITING_LINK_MESSAGE
    inline_markup = await menu.back_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    await ParsingPhones.waiting_link.set()

'''Кнопка парсинга приватного чата'''

@dp.callback_query_handler(lambda call: 'parsing_private' in call.data)
async def parsing_private_start(callback_query: types.CallbackQuery):
    text = WAITING_PRIVATE_LINK_MESSAGE
    inline_markup = await menu.back_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    await ChatPrivateLink.waiting_link.set()

'''Кнопка писавшие в чат'''

@dp.callback_query_handler(lambda call: 'parsing_messages' in call.data)
async def parsing_activity_start(callback_query: types.CallbackQuery):
    text = 'Отправьте ссылку на чат'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await ParsingMessages.waiting_link.set()

'''Запрос фильтра по сообщениям'''

@dp.message_handler(state=ParsingMessages.waiting_link)
async def get_filter_activity(message: types.Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    link = message.text
    if await check_link(link):
        inline_markup = await menu.messages_count_menu()
        text = 'За какое время вам необходимы сообщения?'
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
        await ParsingMessages.count.set()
    else:
        text = WRONG_CHAT_MESSAGE
        inline_markup = await menu.back_menu()
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Прасинг открытого чата'''

@dp.message_handler(state=ChatOpenLink.waiting_link)
async def get_open_report(message: types.Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    state_data = await state.get_data()
    link = state_data.get('waiting_link')
    if await check_link(link):
        ALL_PARTICIPANTS = await request.open_chat_request(link, message.chat.id)
        await create_report.create_open_chat_report(ALL_PARTICIPANTS, 'users')
        await state.finish()
        text = NEXT_PARSING_MESSAGE
        inline_markup = await menu.main_menu()
        target = '*.txt'
        file = glob.glob(target)[0]
        if os.stat(file).st_size == 0:
            await message.answer(NO_USERS_MESSAGE, reply_markup=inline_markup, parse_mode='Markdown')
        else:
            await message.reply_document(open(file, 'rb'))
            await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        text = WRONG_CHAT_MESSAGE
        inline_markup = await menu.back_menu()
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Парсинг по последней активности'''

@dp.callback_query_handler(state=ParsingActive.last_activity)
async def parsing_activity_start(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(last_activity=callback_query.data)
    state_data = await state.get_data()
    link = state_data.get('waiting_link')
    online = state_data.get('last_activity').split('_')[1]
    ALL_PARTICIPANTS = await request.activity_request(link, callback_query.from_user.id, online)
    await create_report.create_open_chat_report(ALL_PARTICIPANTS, 'users') 
    await state.finish()
    target = '*.txt'
    file = glob.glob(target)[0]
    text = NEXT_PARSING_MESSAGE
    inline_markup = await menu.main_menu()
    if os.stat(file).st_size == 0:
            await bot.send_message(callback_query.from_user.id, NO_USERS_MESSAGE, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        await bot.send_document(callback_query.from_user.id, open(file, 'rb'))
        await bot.send_message(callback_query.from_user.id, text, reply_markup=inline_markup)
    
'''Прасинг телефонов'''

@dp.message_handler(state=ParsingPhones.waiting_link)
async def get_phone_numbers(message: types.Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    state_data = await state.get_data()
    link = state_data.get('waiting_link')
    if await check_link(link):
        ALL_PARTICIPANTS = await request.open_chat_request(link, message.chat.id)
        await create_report.create_open_chat_report(ALL_PARTICIPANTS, 'phones')
        target = '*.txt'
        file = glob.glob(target)[0] 
        await state.finish()
        text = NEXT_PARSING_MESSAGE
        inline_markup = await menu.main_menu()
        if os.stat(file).st_size == 0:
            await message.answer(NO_PHONES_MESSAGE, reply_markup=inline_markup, parse_mode='Markdown')
        else:
            await message.reply_document(open(file, 'rb'))
            await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        text = WRONG_CHAT_MESSAGE
        inline_markup = await menu.back_menu()
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Парсинг приватного чата'''

@dp.message_handler(state=ChatPrivateLink.waiting_link)
async def get_private_report(message: types.Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    state_data = await state.get_data()
    link = trim_link(state_data.get('waiting_link'))
    print('@@@@@@@@@', link)
    if await check_private_link(link):
        ALL_PARTICIPANTS = await request.private_chat_request(link, message.chat.id)
        await create_report.create_open_chat_report(ALL_PARTICIPANTS, 'pyrogram')
        await state.finish()
        text = NEXT_PARSING_MESSAGE
        inline_markup = await menu.main_menu()
        target = '*.txt'
        file = glob.glob(target)[0]
        await message.reply_document(open(file, 'rb'))
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        text = WRONG_CHAT_MESSAGE
        inline_markup = await menu.back_menu()
        await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Парсинг по сообщениям'''

@dp.callback_query_handler(state=ParsingMessages.count)
async def parsing_activity_start(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(count=callback_query.data)
    state_data = await state.get_data()
    link = state_data.get('waiting_link')
    link = await trim_link(link)
    count = state_data.get('count').split('_')[1]
    current_time = datetime.now(timezone.utc)
    ALL_PARTICIPANTS = await request.chat_messages_request(link, callback_query.from_user.id, current_time, int(count))
    await create_report.create_open_chat_report(ALL_PARTICIPANTS, 'pyrogram') 
    await state.finish()
    target = '*.txt'
    file = glob.glob(target)[0]
    text = 'Для парсинга следующего чата выберите необходимое действие👇'
    inline_markup = await menu.main_menu()
    await bot.send_document(callback_query.from_user.id, open(file, 'rb'))
    await bot.send_message(callback_query.from_user.id, text, reply_markup=inline_markup)

'''Вызов меню администратора'''                                   

@dp.message_handler(lambda message: orm.check_admin(message.from_user.id) == 1 and message.text == '/admin')
async def get_admin_menu(message: types.Message):
    text = ACTION_CHOICE_MESSAGE
    inline_markup = await menu.admin_menu()
    await message.answer(text, reply_markup=inline_markup)

'''Кнопка рассылки'''

@dp.callback_query_handler(lambda call: 'create_mailing' in call.data)
async def create_mailing(callback_query: types.CallbackQuery):
    text = BROADCAST_TEXT_MESSAGE
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await Mailing.text.set()

'''Рассылка'''

@dp.message_handler(state=Mailing.text)
async def mailing(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text, entity=message.entities)
    state_data = await state.get_data()
    text = state_data.get('text')
    entity = state_data.get('entity')
    users = orm.get_all_users()
    await message.answer(BROADCAST_START_MESSAGE, parse_mode='Markdown')
    count = 0
    count_of_banned = 0
    for user in users:
        try:
            await bot.send_message(user.tg_id, text=text, entities=entity, disable_web_page_preview=True)
            count += 1
            if count == 15:
                asyncio.sleep(USER_PARSE_DELAY)
                count = 0
        except:
            count_of_banned += 1
    answer = f'{BROADCAST_MESSAGE_PART_1}{len(users)}\n{BROADCAST_MESSAGE_PART_2}{len(users)-count_of_banned}\n{BROADCAST_MESSAGE_PART_3}{count_of_banned}'
    orm.add_blocked(count_of_banned)
    await message.answer(answer, parse_mode='Markdown')
    await state.finish()

'''Кнопка выдачи премиум статуса'''

@dp.callback_query_handler(lambda call: 'set_premium' in call.data)
async def button_premium(callback_query: types.CallbackQuery):
    text = ENTER_ID_MESSAGE
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await Get_id_premium.user_id.set()

'''Создание премиум пользователя'''

@dp.message_handler(state=Get_id_premium.user_id)
async def create_premium(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    state_data = await state.get_data()
    user_id = state_data.get('user_id')
    current_time_utc =  datetime.now(timezone.utc)
    target_time = current_time_utc + timedelta(hours=240, minutes=0)
    orm.get_premium(user_id, current_time_utc, target_time)
    await state.finish()
    await bot.send_message(int(user_id), PREMIUM_GRANTED_MESSAGE, parse_mode='Markdown')
    inline_markup = await menu.admin_menu()
    await message.answer(PREMIUM_GRANTED_SUCCESS_MESSAGE, reply_markup=inline_markup)

'''Кнопка дать права администратора'''

@dp.callback_query_handler(lambda call: 'set_admin_previlegies' in call.data)
async def button_admin(callback_query: types.CallbackQuery):
    text = ENTER_ID_MESSAGE
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await Get_id_admin.user_id.set()

'''Создание администратора'''

@dp.message_handler(state=Get_id_admin.user_id)
async def create_admin(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    state_data = await state.get_data()
    user_id = state_data.get('user_id')
    orm.get_admin(user_id)
    await state.finish()
    inline_markup = await menu.admin_menu()
    await message.answer(ADMIN_GRANTED_SUCCESS_MESSAGE, reply_markup=inline_markup)

'''Выдача статистики'''

@dp.callback_query_handler(lambda call: 'stat' in call.data)
async def get_stat(callback_query: types.CallbackQuery):
    stat = orm.stat()
    text = f'Всего пользователей: {stat[0]}\nУдалили чат с ботом: {stat[1]}\n*Количество удаливших чат с ботом обновляется после рассылки*'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')

''' Покупка премиума '''

@dp.callback_query_handler(lambda call: 'buy_premium' in call.data)
async def button_buy(callback_query: types.CallbackQuery):
    await bot.send_invoice(
    callback_query.from_user.id,
    title=PREMIUM_BUY_MESSAGE,
    description=PREMIUM_BUY_DESCRIPTION_MESSAGE,
    provider_token=bot_settings.PAYMENT_TOKEN,
    currency='rub',
    photo_url=bot_settings.IMAGE_URL,
    photo_height=512, 
    photo_width=512,
    photo_size=512,
    is_flexible=False, 
    prices=[bot_settings.PRICE],
    start_parameter='10-days-premium',
    payload='something'
)


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    # прописать валидацию почты или телефона
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    current_time_utc =  datetime.now(timezone.utc)
    target_time = current_time_utc + timedelta(hours=240, minutes=0)
    orm.get_premium(message.from_user.id, current_time_utc, target_time)
    await bot.send_message(message.chat.id,SUCCESS_BUY_MESSAGE)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)