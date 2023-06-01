import asyncio

from TonTools import TonCenterClient, NftCollection
from secret import api_key
from client import *

import requests
import base64


async def tontools():
    client = TonCenterClient(key=api_key)
    collection = NftCollection('EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir', provider=client)
    await collection.update()
    print(collection)


async def get_collection_data(client: TonlibClient, address='EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir'):

    stack = await run_get_method(client, address=address,
                         method='get_collection_data', stack=[])
    next_item_index = int(stack[0][1], 16)
    content = Cell.one_from_boc(base64.b64decode(stack[1][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]
    metadata = requests.get(content).json()
    owner_address = Cell.one_from_boc(base64.b64decode(stack[2][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
    return next_item_index, metadata, owner_address


async def get_nft_address_by_index(client: TonlibClient, collection_address: str = 'EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir', index=7693):
    request_stack = [
        ["num", index]
    ]

    stack = await run_get_method(client, address=collection_address,
                                 method='get_nft_address_by_index', stack=request_stack)

    nft_address = Cell.one_from_boc(base64.b64decode(stack[0][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    return nft_address


async def royalty_params(client: TonlibClient, address: str = 'EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir'):
    stack = await run_get_method(client, address=address, method='royalty_params', stack=[])

    royalty_factor = int(stack[0][1], 16)
    royalty_base = int(stack[1][1], 16)
    royalty_address = Cell.one_from_boc(base64.b64decode(stack[2][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    return royalty_factor, royalty_base, royalty_address


async def get_nft_content(client: TonlibClient, index: int, individual_content: str):
    request_stack = [
        ["num", index],
        ["tvm.Cell", individual_content]
    ]

    stack = await run_get_method(client, address='EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir',
                                 method='get_nft_content', stack=request_stack)

    content = Cell.one_from_boc(base64.b64decode(stack[0][1]['bytes']))

    str = content.bits.get_top_upped_array() + content.refs[0].bits.get_top_upped_array()
    link = str.decode().split('\x01')[-1]
    return link


async def pytonlib():
    client = await get_client(0, False)

    # result = await get_collection_data(client)
    # result = await get_nft_address_by_index(client)
    # result = await royalty_params(client)
    result = await get_nft_content(client, 7693, 'te6cckEBAQEAEAAAHDc2OTMvNzY5My5qc29uLdxv9g==')

    print(result)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())
