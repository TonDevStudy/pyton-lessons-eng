from tonsdk.boc import Cell
from tonsdk.utils import sign_message
import base64
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key


mnemonics1 = ['rather', 'voice', 'zone', 'fold', 'rotate', 'crane', 'roast', 'brave', 'motor', 'kid', 'note', 'squirrel', 'piece', 'home', 'expose', 'bench', 'flame', 'wood', 'person', 'assist', 'vocal', 'bomb', 'dismiss', 'diesel']
pub_k1, priv_k1 = mnemonic_to_wallet_key(mnemonics1)


def sign(b64str_boc: str):
    cell = Cell.one_from_boc(base64.b64decode(b64str_boc))

    """
    validate message
    """
    slice = cell.begin_parse()

    return base64.b64encode(sign_message(cell.bytes_hash(), priv_k1).signature)
