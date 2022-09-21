from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_choice_services_data import choice_services_touch_button


def get_menu_choice_services_all(page):
    '''Группы усоуг'''

    # Функция разбивает на пагинацию список
    def func_chunks_generators(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    position = ['Брови', 'Мужской зал', 'Женские стрижки', 'Окрашивание', 'Укладки', 'Уходы для волос',
                'Ногтевой  сервис', 'Все виды дизайна', 'Депиляция(шугаринг)', 'Депиляция(воск)', 'Наращивание ресниц']
    new_position = list(func_chunks_generators(position, 5))

    inline_kb_full = InlineKeyboardMarkup(row_width=2)

    for ell in new_position[page]:
        inline_kb_full.add(InlineKeyboardButton(text=ell, callback_data=f'touch_choice_services:{ell}:{page}:0'))
    btn_next = InlineKeyboardButton(text='Далее >>>', callback_data=f'touch_this:next_page:{page}')
    btn_back = InlineKeyboardButton(text='<<< Назад', callback_data=f'touch_this:back_page:{page}')
    if page != len(new_position) - 1:
        if page != 0:
            inline_kb_full.add(btn_back, btn_next)
        else:
            inline_kb_full.add(btn_next)
    else:
        inline_kb_full.add(btn_back)
    print(f'inline_kb_full = = = {inline_kb_full}')
    return inline_kb_full


def get_menu_service():
    '''Определенные услуги
    !!!!! Нельзя много данных использовать в callback_data, тянуть данные по id'''

    brow = {
        'Окрашивание бровей': 350,
        'Оформление бровей': 350,
        'Биотатуаж (окрашивание Хной)': 500,
        'Окрашивание ресниц': 300
    }
    men_room = {
        'Модельная Стрижка': 500,
        'креативная': 500,
        'стрижка': 350,
        'стрижка2': 200}

    inline_kb_services = InlineKeyboardMarkup(row_width=1)

    for ell in men_room:
        inline_kb_services.add(InlineKeyboardButton(text=ell,
                                                    callback_data=f'touch_choice_services:main:100:0'))

    print(inline_kb_services)
    return inline_kb_services


def get_menu_choice_services(sum_price):
    print(type(sum_price))
    menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Маникюр покрытие - 1500 руб.',
                                                             callback_data=choice_services_touch_button.new(
                                                                 name='manic',
                                                                 price=1500,
                                                                 sum_price=sum_price
                                                             ))
                                    ],
                                    [
                                        InlineKeyboardButton(text='звёздочки на пальцах - 200 руб.',
                                                             callback_data=choice_services_touch_button.new(
                                                                 name='pedic',
                                                                 price=200,
                                                                 sum_price=sum_price
                                                             ))
                                    ]
                                ])

    return menu
