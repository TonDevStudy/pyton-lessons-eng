import asyncio
import base64
import hashlib
import bitarray

import requests
from TonTools import TonCenterClient, Jetton
from secret import api_key
from client import *
from tonsdk.boc import begin_cell
from tonsdk.utils import Address

async def tontools():
    client = TonCenterClient(key=api_key)
    minter = Jetton('EQDCJL0iQHofcBBvFBHdVG233Ri2V4kCNFgfRT-gqAd3Oc86', provider=client)
    await minter.update()
    print(minter)


def parse_offchain(stack):
    content = \
    Cell.one_from_boc(base64.b64decode(stack[3][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]

    metadata = requests.get('https://ipfs.io/ipfs/' + content.split('ipfs://')[1]).json()
    return metadata


def parse_onchain(cell: Cell):
    parsed_dict = read_dict(cell.begin_parse().read_ref(), 256)
    result = {}
    for i in ['name', 'description', 'image', 'symbol']:
        array = bitarray.bitarray()
        array.frombytes(hashlib.sha256(i.encode()).digest())
        array.to01()
        value = parsed_dict.get(array.to01(), None)
        if value is not None:
            result[i] = value.refs[0].bits.get_top_upped_array().decode().split('\x00')[-1]

    return result


async def pytonlib():
    client = await get_client(0, False)

    stack = await run_get_method(client, method='get_jetton_data', address='EQDCJL0iQHofcBBvFBHdVG233Ri2V4kCNFgfRT-gqAd3Oc86', stack=[])

    total_supply = int(stack[0][1], 16)

    owner_address = Cell.one_from_boc(base64.b64decode(stack[2][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    # content = Cell.one_from_boc(base64.b64decode(stack[3][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]

    # metadata = parse_offchain(stack)
    metadata = parse_onchain(Cell.one_from_boc(base64.b64decode(stack[3][1]['bytes'])))

    print(total_supply, owner_address, metadata)

    await client.close()


async def get_wallet_address():
    jetton_minter = 'EQDCJL0iQHofcBBvFBHdVG233Ri2V4kCNFgfRT-gqAd3Oc86'
    owner_wallet = 'EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG'
    client = await get_client(0, False)

    request_stack = [
        ["tvm.Slice",
         base64.b64encode(begin_cell().store_address(Address(owner_wallet)).end_cell().to_boc()).decode()]
    ]

    stack = await run_get_method(client, method='get_wallet_address', address=jetton_minter, stack=request_stack)
    jetton_wallet = Cell.one_from_boc(base64.b64decode(stack[0][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
    print(jetton_wallet)
    await client.close()


if __name__ == '__main__':
    asyncio.run(get_wallet_address())
