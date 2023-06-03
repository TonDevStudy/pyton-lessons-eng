from tonsdk.contract.token.ft import JettonMinter, JettonWallet
from tonsdk.utils import Address


def create_minter():
    minter = JettonMinter(
        admin_address=Address('EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI'),
        jetton_content_uri='https://raw.githubusercontent.com/TonDevStudy/pyton-lessons-eng/main/lesson_6/metadata.json',
        jetton_wallet_code_hex=JettonWallet.code,
    )

    return minter


def create_mint_tokens_body():
    minter = create_minter()

    body = minter.create_mint_body(
        Address('EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI'),
        jetton_amount=1_000_000 * 10**9, amount=0.02*10**9
    )

    return body
