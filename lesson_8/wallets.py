from pathlib import Path
import asyncio
import requests


from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.crypto import mnemonic_new
from tonsdk.utils import to_nano

from mnemoincs import mnemonics as my_mnemonics
from pytonlib import TonlibClient


def create_wallet():
    mnemonics, pub_k, priv_k, wallet = Wallets.create(WalletVersionEnum.v3r2, workchain=0)

    return wallet


def import_wallet(mnemoincs):
    mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemoincs)

    return wallet


async def get_client():
    ton_config = requests.get('https://ton.org/global.config.json').json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    # init TonlibClient
    client = TonlibClient(ls_index=2,  # choose LiteServer index to connect
                          config=ton_config,
                          keystore=keystore_dir)

    # init tonlibjson
    await client.init()

    return client


async def deploy_wallet():
    wallet = import_wallet(my_mnemonics)

    boc = wallet.create_init_external_message()['message'].to_boc(False)

    client = await get_client()

    await client.raw_send_message(boc)

    await client.close()


async def deploy_wallet_internal():

    new_wallet = create_wallet()

    state_init = new_wallet.create_state_init()['state_init']

    wallet = import_wallet(my_mnemonics)

    boc = wallet.create_transfer_message(
        to_addr=new_wallet.address.to_string(),
        amount=to_nano(0.05, 'ton'),
        seqno=1,
        state_init=state_init
    )['message'].to_boc(False)

    client = await get_client()

    await client.raw_send_message(boc)

    await client.close()


if __name__ == '__main__':

    asyncio.run(deploy_wallet_internal())
