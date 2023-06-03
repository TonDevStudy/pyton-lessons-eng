from TonTools import TonCenterClient, Wallet
import asyncio

from secret import api_key
from client import *
from wallets import import_wallet
from mnemoincs import mnemonics
from mint_bodies import *


async def burn():
    client = await get_client(0, False)

    wallet = import_wallet(mnemonics)

    body = JettonWallet().create_burn_body(
        jetton_amount=100_000*10**9,
    )

    query = wallet.create_transfer_message(
        to_addr='EQCOsF1sD90GgKmy0wAlxMkj1CTDp4WKrPuFJxF1adTIPvEG',
        seqno= await get_seqno(client, wallet.address.to_string()),
        payload=body,
        amount=0.03*10**9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


async def revoke_rights():
    client = await get_client(0, False)

    wallet = import_wallet(mnemonics)

    body = JettonMinter().create_change_admin_body(
        new_admin_address=Address('EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'),
    )

    query = wallet.create_transfer_message(
        to_addr='EQDY5L5YuNUp-Tohu-Fqetpz0R26v8e7H0FXRjp2whL4QLWh',
        seqno=await get_seqno(client, wallet.address.to_string()),
        payload=body,
        amount=0.03 * 10 ** 9
    )

    await client.raw_send_message(query['message'].to_boc(False))

    await client.close()


if __name__ == '__main__':
    asyncio.run(revoke_rights())
