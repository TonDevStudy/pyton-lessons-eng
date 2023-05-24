import asyncio

import requests

from client import get_client
import random


async def is_archival(ls_index: int):
    client = await get_client(ls_index)
    try:
        await client.get_block_transactions(-1, -9223372036854775808, random.randint(2, 4096), count=10)
        print(ls_index, 'is archival!')
    except:
        print(ls_index, 'is not archival!')
    await client.close()


async def main():
    ton_config = requests.get('https://ton.org/global.config.json').json()

    amount = len(ton_config['liteservers'])

    # client = await get_client(0)
    # last = (await client.get_masterchain_info())['last']
    # print(last)

    for i in range(amount):
        await is_archival(i)


if __name__ == '__main__':
    asyncio.run(main())
