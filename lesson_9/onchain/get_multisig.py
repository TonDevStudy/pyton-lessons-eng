import asyncio

from client import *
from tonsdk.boc import Cell
from tonsdk.contract.wallet import MultiSigWallet
import base64


async def get_data(client: TonlibClient, address: str):

    data = (await client.raw_get_account_state(address))['data']
    cell_data = Cell.one_from_boc(base64.b64decode(data))
    slice = cell_data.begin_parse()

    wallet_id = slice.read_uint(32)
    n, k = slice.read_uint(8), slice.read_uint(8)
    slice.skip_bits(64)
    owners = read_dict(slice.load_dict(), 8)

    public_keys = []
    for owner in owners.values():
        public_keys.append(owner.begin_parse().read_bytes(32))

    return {
        'wallet_id': wallet_id,
        'n': n,
        'k': k,
        'public_keys': public_keys
    }


async def get_multisig(client: TonlibClient, address: str):
    data = await get_data(client, address)

    wallet = MultiSigWallet(public_keys=data['public_keys'], k=data['k'], wallet_id=data['wallet_id'])

    return wallet


async def main():
    client = await get_client(0, False)
    wallet = await get_multisig(client, 'EQCOpgZNmHhDe4nuZY6aQh3sgqgwgTBtCL4kZPYTDTDlZY_Y')
    print(wallet.address.to_string(True, True, True))
    await client.close()

if __name__ == '__main__':
    asyncio.run(main())
