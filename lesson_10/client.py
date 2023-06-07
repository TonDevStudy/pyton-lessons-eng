import asyncio

import bitarray
from pytonlib import TonlibClient
from tonsdk.boc import Cell

import requests
from pathlib import Path
import json
from tvm_valuetypes import deserialize_boc, parse_hashmap


async def get_client() -> TonlibClient:
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir, tonlib_timeout=10)
    await client.init()

    return client


async def test_client():
    client = await get_client()

    print(await client.get_masterchain_info())

    await client.close()


if __name__ == '__main__':
    asyncio.run(test_client())
