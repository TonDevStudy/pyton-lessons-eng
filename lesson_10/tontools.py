import asyncio

from TonTools import Contract, TonCenterClient


async def main():
    client = TonCenterClient(base_url='http://84.54.47.174:80/')
    contract = Contract(address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N', provider=client)
    print(await contract.get_balance())


if __name__ == '__main__':
    asyncio.run(main())
