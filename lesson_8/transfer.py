import asyncio

from wallets import import_wallet
from mnemoincs import mnemonics
from client import *

from tonsdk.contract.wallet import Wallets, WalletVersionEnum


async def main():
    _, _, _, hv_wallet = Wallets.from_mnemonics(version=WalletVersionEnum.hv2, mnemonics=mnemonics)

    recieps = [
        {
            'address': 'EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
            'payload': 'comment 1',
            'send_mode': 3,
            'amount': 0.0001*10**9
        },
        {
            'address': 'EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT',
            'payload': 'comment 2',
            'send_mode': 3,
            'amount': 0.0001 * 10 ** 9
        }
    ] * 10

    client = await get_client(7, False)

    query = hv_wallet.create_transfer_message(
        recipients_list=recieps,
        query_id=0
    )

    print(query['query_id'])

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()

# 7241219937983791104
# 7241220814157119488
if __name__ == '__main__':
    asyncio.run(main())
