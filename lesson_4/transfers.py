import asyncio

from TonTools import TonCenterClient, Wallet
from secret import api_key

from lesson_5.client import *
from wallets import import_wallet
from mnemoincs import mnemonics
from tonsdk.contract.token.nft import NFTItem
from tonsdk.utils import Address


async def tontools():
    client = TonCenterClient(api_key)

    wallet = Wallet(provider=client, mnemonics=mnemonics, version='v3r2')

    await wallet.transfer_nft(
        destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
        nft_address='EQDL3cMdF72OKdKStvDXxpz2nsR1Y7tFx9sY5XrcwpEgBf3e',
        fee=0.06
    )


async def pytonlib():
    client = await get_client(0, False)

    wallet = import_wallet(mnemonics)

    body = NFTItem().create_transfer_body(
        new_owner_address=Address('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'),
    )

    query = wallet.create_transfer_message(
        to_addr='EQBafcMuCbIGwXkto1aWzVeQjzZVMtU_olVfQK7wElrwxBXr',
        seqno=await get_seqno(client, wallet.address.to_string()),
        payload=body,
        amount=0.06*10**9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())
