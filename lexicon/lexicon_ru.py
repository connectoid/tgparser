""" Тексты командного меню """

COMMAND_START = {'/start': 'Главное меню'}

""" Тексты кнопок """

TO_MAIN_MENU_BUTTON = '⬅️ В главное меню'
PARSE_OPEN_CHAT_BUTTON = '🔍Спарсить открытый чат'
PREMIUM_FUNCTIONS_BUTTON = '🔒Premium функции'
BUY_PREMIUM_BUTTON = '👑Купить премиум статус'
BY_ACTIVITY_BUTTON = '📆По дате последнего посещения'
PHONES_BUTTON = '📱Моб. телефоны'
WAS_RECENTLY_BUTTON = 'Был(а) недавно'
WAS_ONWEEK_BUTTON = 'Был(а) на этой неделе'
MAKE_BROADCAST_BUTTON = 'Создать рассылку'
STAT_BUTTON = 'Статистика'
GRANT_ADMIN_BUTTON = 'Дать права админа'
GRANT_PREMIUM_BUTTON = 'Дать премиум статус'
PRIVATE_BUTTON = '🔒Приватный чат'
WRITING_USERS_BUTTON = '✍️Парсинг писавших в чат'
LAST_100_BUTTON = 'Последние 100 сообщений'
LAST_500_BUTTON = 'Последние 500 сообщений'
LAST_1000_BUTTON = 'Последние 1000 сообщений'


""" Тексты сообщений """

HELLO_MESSAGE = 'Привет! Я могу спарсить любой чат\nВыбери необходимое действие👇'
WAITING_LINK_MESSAGE = 'Отправьте ссылку на ваш чат в формате *t.mе/durоv* или *@durоv*'
WAITING_PRIVATE_LINK_MESSAGE = 'Отправьте ссылку на приватный чат в формате *t.mе/durоv* или *@durоv*. '\
    'Убедитесь, что ссылка верная. Нерабочие ссылки игнорируются.'
WRONG_CHAT_MESSAGE = 'Такого чата не существует (возможно отправлена ссылка на канал, закрытый чат или '\
    'пользователя), для парсинга закрытых чатов и каналов воспользуйтесь Премиум функциями в главном меню. '\
    'Отправьте ссылку на открытый чат в формате *t.mе/durоv* или *@durоv* '\
    'или вернитесь в Главное меню'
PREMIUM_CHOICE_MESSAGE = 'Выберите необходимый вариант из списка'
PREMIUM_NEED_MESSAGE = 'Данная функция доступна только премиум пользователям'
ACTIVITY_PERIOD_MESSAGE = 'За какой промежуток времени пользователи должны были быть онлайн?'
NEXT_PARSING_MESSAGE = 'Для парсинга следующего чата выберите необходимое действие👇'
NO_PHONES_MESSAGE = 'Пользователей с нескрытым телефоном не найдено'
NO_USERS_MESSAGE = 'Пользователей не найдено'
ACTION_CHOICE_MESSAGE = 'Выберите необходимое действие'
BROADCAST_TEXT_MESSAGE = 'Введите текст, который хотите разослать'
BROADCAST_START_MESSAGE = 'Начинаю рассылку'
BROADCAST_MESSAGE_PART_1 = 'Отправка рыссылки завершена\nВсего пользователей: '
BROADCAST_MESSAGE_PART_2 = 'Отправлено успешно: '
BROADCAST_MESSAGE_PART_3 = 'Удалили чат с ботом: '
ENTER_ID_MESSAGE = 'Введите id пользователя'
PREMIUM_GRANTED_MESSAGE = 'Вам выдан премиум-статус на 10 дней'
PREMIUM_GRANTED_SUCCESS_MESSAGE = 'Премиум статус выдан успешно'
ADMIN_GRANTED_SUCCESS_MESSAGE = 'Права администратора выданы успешно'
PREMIUM_BUY_MESSAGE = 'Покупка премиум статуса'
PREMIUM_BUY_DESCRIPTION_MESSAGE = 'Покупка премиум статуса на 10 дней'
SUCCESS_BUY_MESSAGE = 'Оплата прошла успешно'
STARTING_PARSING_MESSAGE = 'Начинаю парсинг, это может занять от несколких секунд до нескльких минут ⏱'
PARSING_PROGRESS_MESSAGE = 'Идёт парсинг: 0% [..........]'
PARSING_MESSAGE = 'Идёт парсинг: '