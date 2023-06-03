from TonTools import TonCenterClient, Wallet
import asyncio

from secret import api_key
from client import *
from wallets import import_wallet
from mnemoincs import mnemonics
from mint_bodies import *


async def tontools():
    client = TonCenterClient(key=api_key)
    wallet = Wallet(mnemonics=mnemonics, version='v3r2', provider=client)

    resp = await wallet.transfer_jetton_by_jetton_wallet(destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
                            jettons_amount=1000, jetton_wallet='EQCOsF1sD90GgKmy0wAlxMkj1CTDp4WKrPuFJxF1adTIPvEG')

    resp = await wallet.transfer_jetton(
        destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
        jettons_amount=1000, jetton_master_address='EQDY5L5YuNUp-Tohu-Fqetpz0R26v8e7H0FXRjp2whL4QLWh')
    print(resp)


async def pytonlib():
    client = await get_client(0, False)

    wallet = import_wallet(mnemonics)

    body = JettonWallet().create_transfer_body(
        to_address=Address('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'),
        jetton_amount=1000*10**9,
    )

    query = wallet.create_transfer_message(
        to_addr='EQCOsF1sD90GgKmy0wAlxMkj1CTDp4WKrPuFJxF1adTIPvEG',
        seqno= await get_seqno(client, wallet.address.to_string()),
        payload=body,
        amount=0.06*10**9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib())

