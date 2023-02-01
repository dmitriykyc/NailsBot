from aiogram import Dispatcher, types


def register_about_us_handlers(dp: Dispatcher):
    @dp.message_handler(text='О нас')
    async def about_us(message: types.Message):
        await message.answer_photo(
            photo='AgACAgIAAxkBAAIN02M_PRukNN6IGUi5vdDvKAPaGglYAAIsxDEbTZH4SYrwWgTo2e8iAQADAgADcwADKgQ',
            caption=f'Приветствуем Вас в чат боте салона: <b>«Иль де Франс»</b>💅\n\n'
                    f'‼ Это полностью демонстрационный бот, можете смело жать на все кнопки 😉\n\n'
                    f'Мы находимы по адресу:\n'
                    f'📍 г.Москва, ул.Охотный ряд, д. 1\n\n'
                    f'В этом чат боте Вы можете записаться на услуги, управлять своими записями, '
                    f'так же здесь будут появляться самые сочные предложения от нашего салона '
                    f'и мы обязательно напомним о Вашем посещении накануне.\n\n'
                    f'Приятного пользования!\n')

    @dp.message_handler(text="🤩Как сделать такого бота себе?🤩")
    async def lead_order(message: types.Message):
        print(message)
        text_order = f'Заявка от @{message["from"]["username"]}\n' \
                     f'tg://user?id={message["from"]["id"]}\n\n' \
                     f'{message["from"]}'
        await dp.bot.send_message(354585871, text_order)
        await message.answer('👍 Спасибо за проявленный интерес!\n\n'
                             'Наши разработчики скоро с Вами свяжутся.')

    @dp.message_handler(text='🤔Что ещё умеет этот бот?🤔')
    async def whats_bot(message: types.Message):
        await message.answer('Вся прелесть этого бота в том, что он будет напоминать '
                             'клиентам, спустя время что пора обновить маникюр, сделать прическу и т.д., например'
                             ' через 2 недели после последнего посещения.\n\n'
                             'Вся информация будет связана с Вашим Yclients или другими сервисами, поэтому, здесь будет'
                             ' только актуальная информация о мастерах и свободных датах.\n\n'
                             'Так же бот будет напоминать накануне о записи и повторно дублировать напоминание.\n\n'
                             'В боте можно делать рассылку по клиентам о предстоящих акциях, новых филиалах и т.д.'
                             '\n\nМы готовы рассмотреть Ваши пожелания и внедрить удобный для Вас функционал. ')


    @dp.message_handler()
    async def all_message(message: types.Message):
        print(message)
        await message.answer('I do not know this text, contact the support')
