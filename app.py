import telebot
from config import keys, TOKEN
from extensions import ConvertionException, APIException
# Создание объекта бота с использованием токена
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    # Обработчик команд /start и /help
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    # Обработчик команды /values
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def get_price(message: telebot.types.Message):
    # Обработчик текстовых сообщений
    try:
        # Разбиваем сообщение пользователя на составляющие
        values = message.text.split(' ')
        # Проверка количества параметров
        if len(values) > 3:
            raise ConvertionException('Слишком много параметров.')
        if len(values) < 3:
            raise ConvertionException('Слишком мало параметров.')
        # Извлечение валют и суммы
        quote, base, amount = values
        # Вызов метода для конвертации валют из расширения
        total_base = APIException.get_price(base, quote, amount)
    except ConvertionException as e:
        # Обработка исключения ConvertionException
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        # Обработка остальных исключений
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # Отправка результата пользователю
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

# Запуск бота в режиме none stop
bot.polling(none_stop=True)