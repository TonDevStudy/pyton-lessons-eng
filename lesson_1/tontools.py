import asyncio

from TonTools import Wallet, TonCenterClient, Contract
from mnemoincs import mnemonics
from secret import api_key


async def main():

    client = TonCenterClient(api_key)

    wallet = Wallet(provider=client, mnemonics=mnemonics, version='v3r2')

    # print(await wallet.transfer_ton('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N', 0.01, message='hello from python lessons'))

    print(wallet.address)

    print(await wallet.get_state())

    contract = Contract(provider=client, address='EQD4ziUFradzeZBLGVpDqoBE5GegeQjzIqC8fdOEXicsi35n')

    print(await contract.run_get_method(method='get_contract_storage_data', stack=[]))


if __name__ == '__main__':
    asyncio.run(main())
