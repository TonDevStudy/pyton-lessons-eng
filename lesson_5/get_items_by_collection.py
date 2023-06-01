import asyncio

from parse_collection import get_nft_address_by_index, get_collection_data
from client import *


async def main():
    collection_address = 'EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir'
    client = await get_client(0, False)
    next_item_index, _, _ =await get_collection_data(client, collection_address)

    for i in range(0, next_item_index):
        address = await get_nft_address_by_index(client, collection_address, i)
        print(i, address)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
