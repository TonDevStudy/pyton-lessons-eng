from tonsdk.boc import Cell
from tonsdk.boc import begin_cell
from tonsdk.utils import Address
from bitarray import bitarray


def cell_create():
    cell = begin_cell()\
        .store_uint(15, 32)\
        .store_address(Address('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'))\
        .store_coins(1.123 * 10*10**9)\
        .end_cell()
    return cell


def parse_cell_bitarray():
    a = bitarray()
    cell = cell_create()
    a.frombytes(cell.bits.get_top_upped_array())

    num = int(a[:32].to01(), 2)
    del a[:32]
    print(num)

    del a[:3]

    wc = hex(int(a[:8].to01(), 2)).replace('0x', '')

    del a[:8]

    hash_part = a[:256].tobytes().hex()
    del a[:256]

    print(wc, hash_part)

    print(Address(str(wc) + ':' + hash_part).to_string(True, True, True))

    l = int(a[:4].to01(), 2)
    del a[:4]

    print(int(a[:l * 8].to01(), 2))
    del a[:l * 8]


def parse_cell_tonsdk():
    cell = cell_create()

    slice = cell.begin_parse()

    num = slice.read_uint(32)

    address = slice.read_msg_addr()

    grams = slice.read_coins()

    print(num, address.to_string(True, True, True), grams)


if __name__ == '__main__':
    parse_cell_bitarray()

