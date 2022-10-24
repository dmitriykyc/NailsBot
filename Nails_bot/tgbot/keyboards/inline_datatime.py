from datetime import datetime
import calendar

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_datetime_data import create_datetime, ignore_callback


def get_menu_years(way):
    '''Выбор года'''
    year = datetime.now().year
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='2022',
                                                             callback_data=create_datetime.new(
                                                                 step='get_year',
                                                                 master='Елена',
                                                                 year=year,
                                                                 month='None',
                                                                 day='None',
                                                                 time='None',
                                                                 way=way
                                                             )),
                                        InlineKeyboardButton(text='2023',
                                                             callback_data=create_datetime.new(
                                                                 step='get_year',
                                                                 master='Елена',
                                                                 year=year + 1,
                                                                 month='None',
                                                                 day='None',
                                                                 time='None',
                                                                 way=way
                                                             ))
                                    ]
                                ])

    return menu


def get_menu_month(year, way):
    '''Выбор месяца'''
    now_month = datetime.now().month
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    if now_month > 9:
        months_new = months[now_month - 1:]
    else:
        months_new = months[now_month - 1:now_month + 2]

    menu2 = InlineKeyboardMarkup(row_width=2,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text=ell,
                                                              callback_data=create_datetime.new(
                                                                  step='get_month',
                                                                  master='Елена',
                                                                  year=year,
                                                                  month=months.index(ell) + 1,
                                                                  day='None',
                                                                  time='None',
                                                                  way=way
                                                              )) for ell in months_new
                                     ]
                                 ])

    return menu2


def get_menu_day(year, month, way):
    '''Выбор дня'''
    inline_kb = InlineKeyboardMarkup(row_width=7)
    inline_kb.row()
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback.new(
            step='IGNORE'
        )))
    #
    month_calendar = calendar.monthcalendar(int(year), int(month))

    for week in month_calendar:
        inline_kb.row()
        for day in week:
            if day == 0:
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback.new(step='IGNORE')))
                continue
            inline_kb.insert(InlineKeyboardButton(
                str(day), callback_data=create_datetime.new(
                    step='get_day',
                    master='Елена',
                    year=year,
                    month=month,
                    day=day,
                    time='None',
                    way=way
                )
            ))
    return inline_kb


def get_menu_time(year, month, day, way):
    list_time = ['10:00', '11:00', '15:00', '18:00', '19:00', '21:00']
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='10:00',
                                                             callback_data=create_datetime.new(
                                                                 step='get_time',
                                                                 master='Елена',
                                                                 year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time='10-00',
                                                                 way=way
                                                             )),
                                        InlineKeyboardButton(text='14:00',
                                                             callback_data=create_datetime.new(
                                                                 step='get_time',
                                                                 master='Елена',
                                                                 year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time='14-00',
                                                                 way=way
                                                             )),
                                        InlineKeyboardButton(text='16:30',
                                                             callback_data=create_datetime.new(
                                                                 step='get_time',
                                                                 master='Елена',
                                                                 year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time='16-30',
                                                                 way=way
                                                             )),
                                        InlineKeyboardButton(text='19:15',
                                                             callback_data=create_datetime.new(
                                                                 step='get_time',
                                                                 master='Елена',
                                                                 year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time='19-15',
                                                                 way=way
                                                             ))
                                    ]
                                ])

    return menu
