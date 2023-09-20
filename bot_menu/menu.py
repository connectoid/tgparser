from aiogram import types

from lexicon.lexicon_ru import *

async def main_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text=PARSE_OPEN_CHAT_BUTTON, 
            callback_data='parsing_open_start'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=PREMIUM_FUNCTIONS_BUTTON, 
            callback_data='premium_menu'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=BUY_PREMIUM_BUTTON, 
            callback_data='buy_premium'
    ))
    return inline_markup

async def premium_parsing_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text=BY_ACTIVITY_BUTTON, 
            callback_data='parsing_activity'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text=PHONES_BUTTON, 
        callback_data='phones'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text=PRIVATE_BUTTON, 
        callback_data='parsing_private'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text=WRITING_USERS_BUTTON, 
        callback_data='parsing_messages'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text=TO_MAIN_MENU_BUTTON, 
        callback_data='main_menu'
    ))
    return inline_markup


async def messages_count_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text=LAST_100_BUTTON, 
            callback_data='messages_100'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=LAST_500_BUTTON, 
            callback_data='messages_500'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=LAST_1000_BUTTON, 
            callback_data='messages_1000'
    ))
    return inline_markup


async def back_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
        text=TO_MAIN_MENU_BUTTON, 
        callback_data='back_to_main_menu'
    ))
    return inline_markup

async def last_active_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text=WAS_RECENTLY_BUTTON, 
            callback_data='online_recently'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=WAS_ONWEEK_BUTTON, 
            callback_data='online_week'
    ))
    return inline_markup

async def admin_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text=MAKE_BROADCAST_BUTTON, 
            callback_data='create_mailing'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=STAT_BUTTON, 
            callback_data='stat'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text=GRANT_ADMIN_BUTTON, 
            callback_data='set_admin_previlegies'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text=GRANT_PREMIUM_BUTTON, 
        callback_data='set_premium'
    ))
    return inline_markup