import asyncio

from client import get_client
from pytonlib import TonlibClient


async def get_block(wc: int, shard: int, seqno: int, client: TonlibClient):
    return (await client.get_block_transactions(wc, shard, seqno, count=40))['transactions']


async def get_transactions(tr_ids: list, client: TonlibClient):
    result = []
    for tr_id in tr_ids:
        trs = await client.get_transactions(account=tr_id['account'],
                                            from_transaction_lt=tr_id['lt'],
                                            from_transaction_hash=tr_id['hash'],
                                            limit=1)
        result.append(trs[0])
    return result


async def last_master_blocks(client: TonlibClient):

    while True:
        master_data = (await client.get_masterchain_info())['last']
        print(master_data['seqno'])
        trs = await get_transactions(await get_block(master_data['workchain'], master_data['shard'], master_data['seqno'], client), client)
        print(trs)


async def last_basechain_blocks(client: TonlibClient):
    while True:
        master_data = (await client.get_masterchain_info())['last']
        print(master_data['seqno'])
        base_data = (await client.get_shards(master_seqno=master_data['seqno']))['shards'][0]
        print(base_data['seqno'])
        trs = await get_transactions(
            await get_block(base_data['workchain'], base_data['shard'], base_data['seqno'], client), client)
        print(trs)


async def main():
    client = await get_client(0)

    # tr_ids = await get_block(-1, -9223372036854775808, 29000000, client)
    # print(await get_transactions(tr_ids, client))

    # await last_master_blocks(client)
    await last_basechain_blocks(client)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
