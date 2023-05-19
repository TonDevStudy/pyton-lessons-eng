import asyncio

from pytonlib import TonlibClient
from tonsdk.utils import to_nano, b64str_to_bytes

from wallets import get_client, import_wallet, my_mnemonics

from tonsdk.boc import begin_cell, Cell



async def run_get_method(client, address:str, method:str, stack: list=[]):

    stack = (await client.raw_run_method(address, method, stack))['stack']

    return stack


async def main():

    payload = begin_cell().store_uint(16, 32).end_cell()

    wallet = import_wallet(my_mnemonics)

    client = await get_client()

    seqno = int((await run_get_method(client, address='EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI', method='seqno', stack=[]))[0][1], 16)

    boc = wallet.create_transfer_message(
        to_addr='EQD4ziUFradzeZBLGVpDqoBE5GegeQjzIqC8fdOEXicsi35n',
        amount=to_nano(0.03, 'ton'),
        seqno=seqno,
        payload=payload
    )['message'].to_boc(False)

    # await client.raw_send_message(boc)

    stack = await run_get_method(client, address='EQD4ziUFradzeZBLGVpDqoBE5GegeQjzIqC8fdOEXicsi35n', method='get_contract_storage_data', stack=[])

    address = Cell.one_from_boc(b64str_to_bytes(stack[1][1]['bytes'])).begin_parse().read_msg_addr().to_string(True, True, True)

    await client.close()

    print(stack)
    print(address)


if __name__ == '__main__':
    asyncio.run(main())
