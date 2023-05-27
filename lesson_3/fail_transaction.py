import asyncio

from mnemoincs import mnemonics

from pytonlib import TonlibClient
from wallets import import_wallet, get_client


async def get_seqno(client: TonlibClient, address:str):
    return int((await client.raw_run_method(
        method='seqno',
        address=address,
        stack_data=[]
    ))['stack'][0][1], 16)


async def main():
    client = await get_client(5)

    wallet = import_wallet(mnemonics)

    query = wallet.create_transfer_message(
        to_addr='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
        amount=30 * 10**9,
        seqno=await get_seqno(client, address=wallet.address.to_string()),
        send_mode=3
    )['message']

    await client.raw_send_message(query.to_boc(False))

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())

