import asyncio

from client import *
from wallets import import_wallet
from mnemoincs import mnemonics
from mint_bodies import *


async def deploy_minter():
    client = await get_client(0, False)

    minter = create_minter()

    wallet = import_wallet(mnemonics)

    state_init = minter.create_state_init()['state_init']
    minter_address = minter.address.to_string(True, True, True)

    query = wallet.create_transfer_message(
        to_addr=minter_address,
        state_init=state_init,
        seqno=await get_seqno(client, wallet.address.to_string()),
        amount=0.03 * 10 ** 9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


async def mint_tokens():
    client = await get_client(0, False)

    minter = create_minter()

    wallet = import_wallet(mnemonics)

    body = create_mint_tokens_body()
    minter_address = minter.address.to_string(True, True, True)

    query = wallet.create_transfer_message(
        to_addr=minter_address,
        payload=body,
        seqno=await get_seqno(client, wallet.address.to_string()),
        amount=0.05 * 10 ** 9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


if __name__ == '__main__':
    asyncio.run(mint_tokens())
