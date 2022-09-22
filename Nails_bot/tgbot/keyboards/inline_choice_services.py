from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_choice_services_data import choice_services_touch_button, \
    category_services_touch_button
from Nails_bot.tgbot.services.db_api import db_commands


def get_menu_choice_services_all(page, category_all):
    '''Группы усоуг'''
    # # Функция разбивает на пагинацию список
    # def func_chunks_generators(lst, n):
    #     for i in range(0, len(lst), n):
    #         yield lst[i: i + n]

    # Функция разбивает на пагинацию словарь
    def slice_data(my_dict, step):
        res = []
        len_item = len(my_dict)
        two_res = {}
        num = 0
        for one, two in my_dict.items():
            num += 1
            two_res[one] = two
            if len(two_res) == step:
                res.append(two_res)
                two_res = {}
            if num == len_item and len(two_res) != 0:
                res.append(two_res)

        return res

    position = {}
    for ell in category_all:
        position[ell.name] = ell.id
    new_position = list(slice_data(position, 5))
    print(new_position)

    inline_kb_full = InlineKeyboardMarkup(row_width=1)

    for name, id_category in new_position[page].items():
        inline_kb_full.add(InlineKeyboardButton(text=name, callback_data=category_services_touch_button.new(
            id_category=id_category
        )))
    btn_next = InlineKeyboardButton(text='Далее >>>', callback_data=f'touch_this:next_page:{page}')
    btn_back = InlineKeyboardButton(text='<<< Назад', callback_data=f'touch_this:back_page:{page}')
    if page != len(new_position) - 1:
        if page != 0:
            inline_kb_full.add(btn_back, btn_next)
        else:
            inline_kb_full.add(btn_next)
    else:
        inline_kb_full.add(btn_back)
    return inline_kb_full


def get_menu_service(all_services):
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

    for ell in all_services:
        inline_kb_services.add(InlineKeyboardButton(text=f'{ell.name} - {ell.price}',
                                                    callback_data=f'touch_choice_services:main:100:0'))
    return inline_kb_services


def get_menu_choice_services(sum_price):
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
