import asyncio

from tonsdk.contract.wallet import MultiSigWallet, MultiSigOrder, MultiSigOrderBuilder
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key, verify_sign
from tonsdk.utils import Address, bytes_to_b64str, b64str_to_bytes, to_nano, sign_message

from client import *


"""import or generate mnemonics"""
# mnemonics1 = mnemonic_new()
# mnemonics2 = mnemonic_new()
# mnemonics3 = mnemonic_new()
mnemonics1 = ['broken', 'decade', 'unit', 'bird', 'enrich', 'great', 'nurse', 'offer', 'rescue', 'sound', 'pole', 'true', 'dignity', 'buyer', 'provide', 'boil', 'connect', 'universe', 'model', 'add', 'obtain', 'hire', 'gift', 'swim']
mnemonics2 = ['rather', 'voice', 'zone', 'fold', 'rotate', 'crane', 'roast', 'brave', 'motor', 'kid', 'note', 'squirrel', 'piece', 'home', 'expose', 'bench', 'flame', 'wood', 'person', 'assist', 'vocal', 'bomb', 'dismiss', 'diesel']
mnemonics3 = ['author', 'holiday', 'figure', 'luxury', 'leg', 'fringe', 'sibling', 'citizen', 'enforce', 'convince', 'silly', 'girl', 'remove', 'purity', 'sand', 'paper', 'file', 'review', 'window', 'kite', 'illegal', 'allow', 'satisfy', 'wait']


"""get pub and priv keys from mnemonics"""
pub_k0, priv_k0 = mnemonic_to_wallet_key(mnemonics1)
pub_k1, priv_k1 = mnemonic_to_wallet_key(mnemonics2)
pub_k2, priv_k2 = mnemonic_to_wallet_key(mnemonics3)


wallet = MultiSigWallet(public_keys=[pub_k0, pub_k1, pub_k2], k=2, wallet_id=0)


"""create order and add message"""
order1 = MultiSigOrderBuilder(wallet.options["wallet_id"])
message = order1.add_message(to_addr='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N', amount=to_nano('0.01', 'ton'), send_mode=3, payload='hello from python tonsdk')
query_id = order1.query_id  # remember this query id or share this with other owners


"""build and sign order"""
order1b = order1.build()
order1b.sign(0, priv_k0)


"""send boc to blockchain"""
query = wallet.create_transfer_message(order1b, priv_k0)
transfer_boc = query["message"].to_boc(False)


"""wait for transaction processing"""


"""create second order with query id from first step"""
order2 = MultiSigOrderBuilder(wallet.options["wallet_id"], query_id=query_id)


"""add the same message here"""
order2.add_message(to_addr='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N', amount=to_nano('0.01', 'ton'),
                   send_mode=3, payload='hello from python tonsdk')

"""build and sign order"""
order2b = order2.build()
order2b.sign(1, priv_k1)


"""send boc to blockchain"""
query_2 = wallet.create_transfer_message(order2b, priv_k1)
transfer_boc_2 = query_2["message"].to_boc(False)


async def main():
    client = await get_client(0, False)

    await client.raw_send_message(transfer_boc)

    await asyncio.sleep(20)

    await client.raw_send_message(transfer_boc_2)


if __name__ == '__main__':
    asyncio.run(main())
