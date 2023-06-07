import asyncio
from tonsdk.contract.wallet import MultiSigWallet, MultiSigOrder, MultiSigOrderBuilder

from tonsdk.boc import Cell
from tonsdk.utils import sign_message
import base64
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key
from get_multisig import get_multisig
from client import *



mnemonics1 = ['rather', 'voice', 'zone', 'fold', 'rotate', 'crane', 'roast', 'brave', 'motor', 'kid', 'note', 'squirrel', 'piece', 'home', 'expose', 'bench', 'flame', 'wood', 'person', 'assist', 'vocal', 'bomb', 'dismiss', 'diesel']
pub_k1, priv_k1 = mnemonic_to_wallet_key(mnemonics1)


async def get_messages_unsigned_by_id(client: TonlibClient, owner_id):
    stack = await run_get_method(client, address='EQCOpgZNmHhDe4nuZY6aQh3sgqgwgTBtCL4kZPYTDTDlZY_Y',
                         method='get_messages_unsigned_by_id', stack=[["num", owner_id]])
    cell_dict = Cell.one_from_boc(base64.b64decode(stack[0][1]['bytes']))
    hashmap = read_dict(cell_dict, 64)
    return hashmap


async def main():
    client = await get_client(0, False)
    hashmap = await get_messages_unsigned_by_id(client, 1)
    wallet = await get_multisig(client, 'EQCOpgZNmHhDe4nuZY6aQh3sgqgwgTBtCL4kZPYTDTDlZY_Y')

    for query_id, order in hashmap.items():
        order2 = MultiSigOrderBuilder(wallet.options["wallet_id"], query_id=int(query_id, 2))
        order2.add_message_from_cell(order.refs[0], 3)

        """
        validate message
        """

        order2b = order2.build()
        order2b.sign(1, priv_k1)
        query = wallet.create_transfer_message(order2b, priv_k1)
        transfer_boc = query["message"].to_boc(False)
        await client.raw_send_message(transfer_boc)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
