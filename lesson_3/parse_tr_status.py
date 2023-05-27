import asyncio
from TonTools import Contract, TonCenterClient
from secret import api_key
from wallets import get_client

from pytonlib.utils.tlb import Transaction, deserialize_boc, Slice
import base64


async def tontools():
    client = TonCenterClient(api_key)

    contract = Contract(provider=client, address='EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI')

    trs = await contract.get_transactions(limit=10)

    for tr in trs:
        print(tr.to_dict_user_friendly())


async def pytonlib():
    client = await get_client(5)

    trs = await client.get_transactions(
        account='EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI',
        limit=10
    )

    for tr in trs:
        # print(tr)

        cell = deserialize_boc(base64.b64decode(tr['data']))
        # print(cell)

        tr_data = Transaction(Slice(cell))

        ac_ph_code = tr_data.description.action.result_code
        print('action', ac_ph_code)
        if tr_data.description.compute_ph.type != 'tr_phase_compute_skipped':
            compute_ph_code = tr_data.description.compute_ph.exit_code
            print('compute', compute_ph_code)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())
