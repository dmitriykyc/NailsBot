from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline_choice_services_data import choice_services_touch_button, \
    category_services_touch_button, choose_data_and_time
from tgbot.keyboards.inline_datetime_data import create_datetime
from tgbot.services.db_api import db_commands


def get_menu_choice_services_all(page, category_all, way):
    '''Группы усоуг'''

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

    inline_kb_full = InlineKeyboardMarkup(row_width=1)

    for name, id_category in new_position[page].items():
        inline_kb_full.add(InlineKeyboardButton(text=name, callback_data=category_services_touch_button.new(
            id_category=id_category, way=way
        )))
    btn_next = InlineKeyboardButton(text='Далее >>>', callback_data=f'touch_this:next_page:{page}:{way}')
    btn_back = InlineKeyboardButton(text='<<< Назад', callback_data=f'touch_this:back_page:{page}:{way}')
    if page != len(new_position) - 1:
        if page != 0:
            inline_kb_full.add(btn_back, btn_next)
        else:
            inline_kb_full.add(btn_next)
    else:
        inline_kb_full.add(btn_back)
    inline_kb_full.add(InlineKeyboardButton(text='👉 Готово, продолжить', callback_data=choose_data_and_time.new(
        res_choose='hello', go_d_t='False', id_mast='', way=way
    )))
    return inline_kb_full


def get_menu_service(all_services, id_choose_already, way):
    '''Определенные услуги'''
    inline_kb_services = InlineKeyboardMarkup(row_width=1)

    for ell in all_services:
        after_text = '✅ ' if ell.id in id_choose_already else ''
        inline_kb_services.add(InlineKeyboardButton(text=f'{after_text}{ell.name} - {ell.price}',
                                                    callback_data=f'tcs:{ell.id}:{ell.price}:0:{way}'))
    inline_kb_services.add(InlineKeyboardButton(text='↩ Назад к категориям', callback_data=f'back_to_category_{way}'))
    if way == 'stm':
        inline_kb_services.add(
            InlineKeyboardButton(text='👉 Готово, продолжить.', callback_data=choose_data_and_time.new(
                res_choose='hello', go_d_t='False', id_mast='', way=way)))
    else:
        inline_kb_services.add(
            InlineKeyboardButton(text='👉 Готово, продолжить.', callback_data='finish_mts'))
    return inline_kb_services


def get_done_menu(way):
    '''Переход к дате'''
    inline_done_menu = InlineKeyboardMarkup(row_width=1)
    inline_done_menu.add(InlineKeyboardButton(text='👍Всё верно, выбрать дату', callback_data=create_datetime.new(
        step='start',
        master='Elena11',
        year='2022',
        month='',
        day='None',
        time='None',
        way=way)))  # choose_data_and_time.new( res_choose='hello', go_d_t='True', id_mast=''))
    # inline_done_menu.add(InlineKeyboardButton(text='🖌Изменить', callback_data='back_to_category'))

    return inline_done_menu


def get_done_menu_mts(way):
    '''Подтверждение выбранных услуг и переход к дате'''
    inline_done_menu = InlineKeyboardMarkup(row_width=1)
    inline_done_menu.add(InlineKeyboardButton(text='👍 Готово, записаться.',
                                              callback_data='done_make_an_entry'))  # choose_data_and_time.new( res_choose='hello', go_d_t='True', id_mast=''))
    inline_done_menu.add(InlineKeyboardButton(text='🖌 Изменить', callback_data='back_to_category'))

    return inline_done_menu


def get_back_menu_datetime(way):
    ''' Вернуться и изменить дату и время '''
    inline_back_menu = InlineKeyboardMarkup(row_width=1)


# def get_menu_choice_services(sum_price):
#     menu = InlineKeyboardMarkup(row_width=2,
#                                 inline_keyboard=[
#                                     [
#                                         InlineKeyboardButton(text='Маникюр покрытие - 1500 руб.',
#                                                              callback_data=choice_services_touch_button.new(
#                                                                  name='manic',
#                                                                  price=1500,
#                                                                  sum_price=sum_price
#                                                              ))
#                                     ],
#                                     [
#                                         InlineKeyboardButton(text='звёздочки на пальцах - 200 руб.',
#                                                              callback_data=choice_services_touch_button.new(
#                                                                  name='pedic',
#                                                                  price=200,
#                                                                  sum_price=sum_price
#                                                              ))
#                                     ]
#                                 ])
#
#     return menu


def choose_master():
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[[
                                    InlineKeyboardButton(text='Выбрать мастера', callback_data='choose_master')
                                ]])

    return menu


def inline_choose_category(way):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[[
                                    InlineKeyboardButton(text='↩ Нет, изменить дату и время',
                                                         callback_data=create_datetime.new(
                                                             step='start',
                                                             master='Elena11',
                                                             year='2022',
                                                             month='',
                                                             day='None',
                                                             time='None',
                                                             way=way))
                                ], [
                                    InlineKeyboardButton(text='✅ Всё верно, выбрать услуги', callback_data='choose_category')
                                ]])
    return menu

