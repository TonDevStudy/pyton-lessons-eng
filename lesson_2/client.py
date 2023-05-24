import requests
from pathlib import Path
from pytonlib import TonlibClient


async def get_client(ls_index: int):
    ton_config = requests.get('https://ton.org/global.config.json').json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    # init TonlibClient
    client = TonlibClient(ls_index=ls_index,  # choose LiteServer index to connect
                          config=ton_config,
                          keystore=keystore_dir)

    # init tonlibjson
    await client.init()

    return client
