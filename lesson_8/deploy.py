import asyncio

from wallets import import_wallet
from mnemoincs import mnemonics
from client import *

from tonsdk.contract.wallet import Wallets, WalletVersionEnum


async def main():
    wallet = import_wallet(mnemonics)

    _, _, _, hv_wallet = Wallets.from_mnemonics(version=WalletVersionEnum.hv2, mnemonics=mnemonics)
    state_init = hv_wallet.create_state_init()['state_init']

    client = await get_client(7, False)

    query = wallet.create_transfer_message(
        to_addr=hv_wallet.address.to_string(),
        state_init=state_init,
        seqno=await get_seqno(client, wallet.address.to_string()),
        amount=0.5 * 10**9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
