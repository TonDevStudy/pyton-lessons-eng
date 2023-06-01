import asyncio

from lesson_5.client import *
from mint_bodies import *
from wallets import import_wallet
from mnemoincs import mnemonics


async def mint_collection():
    client = await get_client(0, False)

    collection = create_collection()

    wallet = import_wallet(mnemonics)

    state_init = collection.create_state_init()['state_init']
    collection_address = collection.address.to_string(True, True, True)

    query = wallet.create_transfer_message(
        to_addr=collection_address,
        state_init=state_init,
        seqno=await get_seqno(client, wallet.address.to_string()),
        amount=0.03 * 10**9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


async def mint_nft():
    index = 0
    client = await get_client(0, False)

    collection = create_collection()

    wallet = import_wallet(mnemonics)

    body = create_mint_nft_body(index)

    collection_address = collection.address.to_string(True, True, True)

    query = wallet.create_transfer_message(
        to_addr=collection_address,
        seqno=await get_seqno(client, wallet.address.to_string()),
        payload=body,
        amount=0.03 * 10 ** 9
    )
    await client.raw_send_message(query['message'].to_boc(False))
    await client.close()


async def mint_batch_nfts():
    from_index = 5
    client = await get_client(0, False)

    collection = create_collection()

    wallet = import_wallet(mnemonics)

    items_amount = 2
    addresses = [Address('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'), Address('EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT')]
    contents = [f'{i + 1}/meta.json' for i in range(from_index, from_index + items_amount)]

    body = create_batch_nfts_mint_body(from_index, addresses, contents)

    collection_address = collection.address.to_string(True, True, True)

    query = wallet.create_transfer_message(
        to_addr=collection_address,
        seqno=await get_seqno(client, wallet.address.to_string()),
        payload=body,
        amount=0.06 * 10 ** 9
    )
    await client.raw_send_message(query['message'].to_boc(False))
    await client.close()


if __name__ == '__main__':
    asyncio.run(mint_batch_nfts())
