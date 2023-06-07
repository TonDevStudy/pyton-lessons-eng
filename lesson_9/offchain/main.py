import asyncio
import base64

from tonsdk.contract.wallet import MultiSigWallet, MultiSigOrder, MultiSigOrderBuilder
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key
from tonsdk.utils import Address, bytes_to_b64str, b64str_to_bytes, to_nano
from client import *
from  get_multisig import get_multisig
from owner_1 import sign


mnemonics0 = ['broken', 'decade', 'unit', 'bird', 'enrich', 'great', 'nurse', 'offer', 'rescue', 'sound', 'pole', 'true', 'dignity', 'buyer', 'provide', 'boil', 'connect', 'universe', 'model', 'add', 'obtain', 'hire', 'gift', 'swim']
pub_k0, priv_k0 = mnemonic_to_wallet_key(mnemonics0)


async def main():
    client = await get_client(0, False)

    wallet = await get_multisig(client, 'EQCOpgZNmHhDe4nuZY6aQh3sgqgwgTBtCL4kZPYTDTDlZY_Y')

    order1 = MultiSigOrderBuilder(wallet.options["wallet_id"])
    order1.add_message(to_addr='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N', amount=to_nano('0.01', 'ton'), send_mode=3, payload='hello from pyton lessons eng')
    order1b = order1.build()
    # order1b.sign(0, priv_k0)

    signature = sign(base64.b64encode(order1b.payload.to_boc()).decode())

    order1b.add_signature(1, base64.b64decode(signature), wallet)

    query = wallet.create_transfer_message(order1b, priv_k0)
    transfer_boc = query["message"].to_boc(False)
    await client.raw_send_message(transfer_boc)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
