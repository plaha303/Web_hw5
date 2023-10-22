import aiohttp
import asyncio
import json
from datetime import datetime, timedelta


class PrivatBankCurrencyAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_data(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + date) as response:
                if response.status == 200:
                    data = await response.json()
                    return data

    async def get_currency_rates(self, days=10, currencies=['EUR', 'USD']):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        currency_rates = []
        while end_date >= start_date:
            formatted_date = end_date.strftime('%d.%m.%Y')
            data = await self.fetch_data(formatted_date)

            if 'exchangeRate' in data:
                rates = data['exchangeRate']
                currency_rate = {
                    formatted_date: {}
                }
                for currency in currencies:
                    for rate in rates:
                        if rate['currency'] == currency:
                            currency_rate[formatted_date][currency] = {
                                'sale': rate['saleRate'],
                                'purchase': rate['purchaseRate']
                            }
                            break

                currency_rates.append(currency_rate)

            end_date -= timedelta(days=1)
        return currency_rates


def main():
    asyncio.run(get_currency_rates_async())


async def get_currency_rates_async():
    api = PrivatBankCurrencyAPI()
    currencies = ['USD', 'EUR', 'PLN']
    currency_rates = await api.get_currency_rates(currencies=currencies)
    print(json.dumps(currency_rates, indent=2))

if __name__ == '__main__':
    main()
