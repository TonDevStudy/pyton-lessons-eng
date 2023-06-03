import asyncio
import base64
import hashlib
import bitarray

import requests
from TonTools import TonCenterClient, Jetton, JettonWallet


from secret import api_key
from client import *
from tonsdk.boc import begin_cell
from tonsdk.utils import Address


async def tontools():
    client = TonCenterClient(key=api_key)
    wallet = JettonWallet('EQC9QpdKuL0s5kNYdq-ELm-iFw4PUFX-l-FpHLQ12O_AbaPe', provider=client)
    await wallet.update()
    print(wallet)


async def pytonlib():
    client = await get_client(0, False)

    stack = await run_get_method(client, method='get_wallet_data', address='EQC9QpdKuL0s5kNYdq-ELm-iFw4PUFX-l-FpHLQ12O_AbaPe', stack=[])

    balance = int(stack[0][1], 16)

    owner_address = Cell.one_from_boc(base64.b64decode(stack[1][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)
    jetton_master_address = Cell.one_from_boc(base64.b64decode(stack[2][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    print(balance, owner_address, jetton_master_address)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())
