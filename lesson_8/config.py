import asyncio

from wallets import import_wallet
from mnemoincs import mnemonics
from client import *

import base64

from tonsdk.boc import Cell, Slice


def parse_16(slice: Slice):
    max_validators = slice.read_uint(16)
    max_main_validators = slice.read_uint(16)
    min_validators = slice.read_uint(16)

    return {
        'max_validators': max_validators,
        'max_main_validators': max_main_validators,
        'min_validators': min_validators
    }


def parse_17(slice: Slice):
    min_stake = slice.read_coins()
    max_stake = slice.read_coins()
    min_total_stake = slice.read_coins()
    max_stake_factor = slice.read_coins()

    return {
        'min_stake': min_stake/10**9,
        'max_stake': max_stake/10**9,
        'min_total_stake': min_total_stake/10**9,
        'max_stake_factor': max_stake_factor,
    }


def parse_34(slice: Slice):
    slice.skip_bits(8)
    utime_since = slice.read_uint(32)
    utime_until = slice.read_uint(32)
    total = slice.read_uint(16)
    main = slice.read_uint(16)

    return {
        'utime_since': utime_since,
        'utime_until': utime_until,
        'total': total,
        'main': main,
    }


async def main():
    client = await get_client(7, False)

    seqno = (await client.get_masterchain_info())['last']['seqno']

    param16 = Cell.one_from_boc(base64.b64decode((await client.get_config_param(16, seqno))['config']['bytes'])).begin_parse()

    param17 = Cell.one_from_boc(base64.b64decode((await client.get_config_param(17, seqno))['config']['bytes'])).begin_parse()

    param34 = Cell.one_from_boc(base64.b64decode((await client.get_config_param(34, seqno))['config']['bytes'])).begin_parse()


    print(parse_16(param16))
    print(parse_17(param17))
    print(parse_34(param34))


    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
