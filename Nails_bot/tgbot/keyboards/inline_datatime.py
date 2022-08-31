from datetime import datetime
import calendar

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_datetime_data import create_datetime, ignore_callback


def get_menu_years():
    '''Выбор года'''
    year = datetime.now().year
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='2022',
                                                             callback_data=create_datetime.new(
                                                                 step='get_year',
                                                                 master='Elena',
                                                                 year=year,
                                                                 month='None',
                                                                 day='None',
                                                                 time='None'
                                                             )),
                                        InlineKeyboardButton(text='2023',
                                                             callback_data=create_datetime.new(
                                                                 step='get_year',
                                                                 master='Elena',
                                                                 year=year + 1,
                                                                 month='None',
                                                                 day='None',
                                                                 time='None'
                                                             ))
                                    ]
                                ])

    return menu


def get_menu_month(year):
    '''Выбор месяца'''
    if year == str(datetime.now().year):
        now_month = datetime.now().month
        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        if now_month > 9:
            months = months[now_month - 1:]
        else:
            months = months[now_month - 1:now_month + 2]
    else:
        months = ['Январь', 'Февраль', 'Март']

    menu2 = InlineKeyboardMarkup(row_width=2,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text=ell,
                                                              callback_data=create_datetime.new(
                                                                  step='get_month',
                                                                  master='Elena',
                                                                  year=year,
                                                                  month=pos + 1,
                                                                  day='None',
                                                                  time='None'
                                                              )) for pos, ell in enumerate(months)
                                     ]
                                 ])

    return menu2


def get_menu_day(year, month):
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
            if (day == 0):
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback.new(step='IGNORE')))
                continue
            inline_kb.insert(InlineKeyboardButton(
                str(day), callback_data=create_datetime.new(
                    step='get_day',
                    master='Elena',
                    year=year,
                    month=month,
                    day='1',
                    time='None'
                )
            ))
    return inline_kb


def get_menu_time(year, month, day):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='10:00',
                                                             callback_data=create_datetime.new(
                                                                 step='get_time',
                                                                 master='Elena',
                                                                 year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time='10-00'
                                                             )),
                                        InlineKeyboardButton(text='20:00',
                                                             callback_data=create_datetime.new(
                                                                 step='get_time',
                                                                 master='Elena',
                                                                 year=year,
                                                                 month=month,
                                                                 day=day,
                                                                 time='20-00'
                                                             ))
                                    ]
                                ])

    return menu
