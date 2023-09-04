from aiogram import types

async def main_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
        text='Парсить открытый чат',
        callback_data='parsing_open_start'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text='Premium функции',
        callback_data='premium_menu'
    ))
    return inline_markup

async def premium_parsing_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text='📆По дате последнего посещения', 
            callback_data='parsing_activity'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text='📱Моб. телефоны', 
        callback_data='phones'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text='🔙Назад', 
        callback_data='main_menu'
    ))
    return inline_markup

async def last_active_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text='Был(а) недавно', 
            callback_data='online_recently'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text='Был(а) на этой неделе', 
            callback_data='online_week'
    ))
    return inline_markup

async def admin_menu():
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(
            text='Создать рассылку', 
            callback_data='create_mailing'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text='Статистика', 
            callback_data='stat'
    ))
    inline_markup.add(types.InlineKeyboardButton(
            text='Дать права админа', 
            callback_data='set_admin_previlegies'
    ))
    inline_markup.add(types.InlineKeyboardButton(
        text='Дать премиум статус', 
        callback_data='set_premium'
    ))
    return inline_markup