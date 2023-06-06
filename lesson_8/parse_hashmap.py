import asyncio

from wallets import import_wallet
from mnemoincs import mnemonics
from client import *

from tonsdk.contract.wallet import Wallets, WalletVersionEnum


def main():
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

    query = hv_wallet.create_transfer_message(
        recipients_list=recieps,
        query_id=0
    )

    print(query['query_id'])

    message = query['signing_message']

    print(message)

    result = read_dict(message.refs[0], 16)

    print(result)

    print(result['0000000000000000'].refs[0])


if __name__ == '__main__':
    main()
