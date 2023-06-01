from tonsdk.contract.token.nft import NFTItem, NFTCollection
from tonsdk.utils import Address


def create_collection():
    address = Address('EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI')
    collection = NFTCollection(
        royalty=0.055,
        royalty_address=address,
        owner_address=address,
        nft_item_code_hex=NFTItem.code,
        collection_content_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/meta.json',
        nft_item_content_base_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/'
    )
    return collection


def create_mint_nft_body(index):
    collection = create_collection()

    body = collection.create_mint_body(
        index,
        Address('EQB6DGcH-A8zy6U01dqPvKaeeMcnHZO-ztcditMHmNhddmMI'),
        '1/meta.json',
        amount=0.02 * 10**9
    )
    return body


def create_batch_nfts_mint_body(from_index: int, addresses:list, contents: list):
    collection = create_collection()
    contents_and_owners = []
    for i in range(len(addresses)):
        contents_and_owners.append((contents[i], addresses[i]))

    body = collection.create_batch_mint_body(
        from_item_index=from_index,
        contents_and_owners=contents_and_owners,
        amount_per_one=0.01 * 10 ** 9
    )

    return body
