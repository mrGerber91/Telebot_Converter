import json
import requests
from config import keys

# Исключение, возникающее при ошибке конвертации валют
class ConvertionException(Exception):
    pass

# Исключение, возникающее при ошибке API-запроса
class APIException(Exception):
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Проверка на одинаковые валюты в запросе
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            # Получение тикера валюты цитирования из конфигурационного файла
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            # Получение тикера базовой валюты из конфигурационного файла
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            # Попытка преобразовать количество в число
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        # API-запрос для получения курса обмена
        api_url = f'https://open.er-api.com/v6/latest/{base_ticker}'
        response = requests.get(api_url)
        data = response.json()

        # Проверка успешности API-запроса
        if response.status_code != 200:
            raise APIException(f'Не удалось получить данные с сервера. Код ошибки: {response.status_code}')

        # Проверка наличия валюты цитирования в ответе API
        if quote_ticker not in data['rates']:
            raise ConvertionException(f'Не удалось получить курс для валюты {quote}')

        # Расчет конвертированной суммы
        exchange_rate = data['rates'][quote_ticker]
        converted_amount = round(amount * exchange_rate, 2)

        return converted_amount
