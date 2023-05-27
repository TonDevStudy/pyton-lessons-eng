import asyncio
from TonTools import Contract, TonCenterClient
from secret import api_key
from wallets import get_client

from pytonlib.utils.tlb import Transaction, deserialize_boc, Slice
import base64

from tonsdk.boc import Cell


async def tontools():
    client = TonCenterClient(api_key)

    contract = Contract(provider=client, address='EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG')

    trs = await contract.get_transactions(limit=5)

    print(trs[4].to_dict())


    # for tr in trs:
    #     print(tr.to_dict_user_friendly())


async def pytonlib():
    client = await get_client(5)

    trs = await client.get_transactions(
        account='EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG',
        limit=5
    )

    for tr in trs:

        if tr['out_msgs']:
            cell = Cell.one_from_boc(base64.b64decode(tr['out_msgs'][0]['msg_data']['body']))
            slice = cell.begin_parse()
            if len(slice) >= 32:
                op = slice.read_bytes(4).hex()
                if op == '595f07bc':
                    print('burn')
                    slice.skip_bits(64)
                    amount = slice.read_coins()
                    print(amount/10**9)
                if op == '0f8a7ea5':
                    print('transfer')
                    slice.skip_bits(64)
                    amount = slice.read_coins()
                    print(amount / 10 ** 9)
                    print(slice.read_msg_addr().to_string(True, True, True))

            # print(cell)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())
