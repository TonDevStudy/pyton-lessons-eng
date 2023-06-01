import asyncio

from TonTools import TonCenterClient, NftItem
from secret import api_key
from client import *

from parse_collection import get_nft_content

import requests
import base64


async def get_sale_data(client: TonlibClient, address='EQCD1lACPLbCaZ0oO9L3lKZOEq4Y1QeY8XSPv4nS658QEZoi'):
    try:
        stack = await run_get_method(client, address=address,
                             method='get_sale_data', stack=[])
    except:
        return (False, )

    fix_magic = '0x46495850'
    auction_magic = '0x415543'
    if stack[0][1] == fix_magic:
        is_complete = bool(int(stack[1][1], 16))
        created_at = int(stack[2][1], 16)
        marketplace_address = Cell.one_from_boc(base64.b64decode(stack[3][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
        nft_address = Cell.one_from_boc(base64.b64decode(stack[4][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
        nft_owner_address = Cell.one_from_boc(base64.b64decode(stack[5][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
        full_price = int(stack[6][1], 16)

        return True, nft_owner_address, full_price

    elif stack[0][1] == auction_magic:
        is_complete = bool(int(stack[1][1], 16))
        end_at = int(stack[2][1], 16)
        marketplace_address = Cell.one_from_boc(base64.b64decode(stack[3][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
        nft_address = Cell.one_from_boc(base64.b64decode(stack[4][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
        nft_owner_address = Cell.one_from_boc(base64.b64decode(stack[5][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
        last_bid = int(stack[6][1], 16)
        min_bid = int(stack[16][1], 16)
        return True, nft_owner_address, max(last_bid, min_bid)


async def pytonlib():
    client = await get_client(0, False)

    result = await get_sale_data(client, 'EQCD1lACPLbCaZ0oO9L3lKZOEq4Y1QeY8XSPv4nS658QEZoi')

    print(result)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())




