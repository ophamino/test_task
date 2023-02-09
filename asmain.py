import time
import asyncio
from aiohttp import ClientSession


max_price: float = 0
check_hours = time.time()


async def get_info(symbol: str = "XRP"):
    url: str = "https://fapi.binance.com/fapi/v1/ticker/price"
    params: dict[str, str] = {"symbol": symbol + "USDT"}
    async with ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            global max_price
            global check_hours
            if response.status == 200:
                data: dict[str, str] = await response.json()
                current_price = float(data['price'])
                if current_price > max_price:
                    max_price = current_price
                if (max_price - current_price) / max_price >= 0.01:
                    print(f"[WARNING] Цена на {symbol + '/USDT'} упала на 1% от \
                         макимальной цены за последний час")
                if time.time() - check_hours >= 3600:
                    check_hours = time.time()
                    max_price = 0


async def main():
    task = asyncio.create_task(get_info())
    await task


if __name__ == '__main__':
    print('[i] Скрипт запущен!')
    while True:
        asyncio.run(main())
        asyncio.sleep(1)
