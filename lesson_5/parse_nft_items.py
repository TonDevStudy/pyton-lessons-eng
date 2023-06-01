import asyncio

from TonTools import TonCenterClient, NftItem
from secret import api_key
from client import *

from parse_collection import get_nft_content
from parse_sale import get_sale_data

import requests
import base64


async def tontools():
    client = TonCenterClient(key=api_key)
    item = NftItem('EQCM8qfFcQVFGW-_6xGSovpQxBJUakja1LrJ24-vlQThJfUE', provider=client)
    await item.update()
    print(item)


async def get_nft_data(client: TonlibClient, address):

    stack = await run_get_method(client, address=address,
                         method='get_nft_data', stack=[])

    index = int(stack[1][1], 16)

    content_link = await get_nft_content(client, index, stack[4][1]['bytes'])

    metadata = requests.get(content_link).json()

    collection_address = Cell.one_from_boc(base64.b64decode(stack[2][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    owner_address = Cell.one_from_boc(base64.b64decode(stack[3][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    result = await get_sale_data(client, owner_address)
    if result[0]:
        owner_address = result[1]

    return index, collection_address, owner_address, metadata


async def pytonlib():
    client = await get_client(0, False)

    result = await get_nft_data(client, 'EQAj_sI_Gb_IWdFzubAnKxRV7nL18V3KqvBnIf8eLIvH_2j4')

    print(result)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())
