import asyncio

from wallets import import_wallet
from mnemoincs import mnemonics
from client import *

from tonsdk.contract.wallet import Wallets, WalletVersionEnum


async def main(qid: int):
    _, _, _, hv_wallet = Wallets.from_mnemonics(version=WalletVersionEnum.hv2, mnemonics=mnemonics)

    client = await get_client(7, False)

    result = await run_get_method(
        client, address=hv_wallet.address.to_string(),
        method='processed?',
        stack=[["num", qid]]
    )

    print(result)

    await client.close()

#7241219937983791104
if __name__ == '__main__':
    asyncio.run(main(7241220814157119488))
