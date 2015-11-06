from random import random

from blockcypher import (
    create_hd_wallet,
    subscribe_to_wallet_webhook,
    get_wallet_transactions
)

from app.api.core.utils import api
from app.bitcoin.util import generate_address_from_xpub
from app.config import Config
from app.db.user_address import UserAddress
from app.db.address_lookup import AddressLookup
from app.exception import MyBitsException


blockcypher_config = Config.get('blockcypher')
api_key = blockcypher_config.get('api_key')

@api(enforce_user=True)
def add(context, request, api_version, user,
        address=None):

    if not address:
        raise MyBitsException('Parameter `address` missing')


    # Add address to a wallet on BlockCypher
    wallet_name = 'wallet-' + str(int(random() * (2**32 - 1)))
    create_hd_wallet(wallet_name, address, api_key)

    # Query BlockCypher to get the used addresses
    used_addresses = set(map(lambda tx: tx['address'], get_wallet_transactions(wallet_name, api_key)['txrefs']))

    # Generate addresses (up to 100) until we find all the one used
    sub_addresses = []
    indexes = []
    found = set()
    for i in xrange(100):
        sub_address = generate_address_from_xpub(address, i)
        sub_addresses.append(sub_address)
        indexes.append(i)
        if sub_address in used_addresses:
            found.add(sub_address)
            if found == used_addresses:
                break

    if len(found) == 0:
        # If we arrive here it means the user used an address that is at the index
        # 100 or more without using any of the previous ones.
        # TODO - Having an alert so we can take a look at the issue
        pass

    # Then generate 10 more
    for i in xrange(len(sub_addresses), len(sub_addresses) + 10):
        sub_address = generate_address_from_xpub(address, i)
        sub_addresses.append(sub_address)
        indexes.append(i)

    # Add the addresses to the lookup table
    AddressLookup.multi_add(user.user_id, sub_addresses, indexes, wallet_name, address)

    # Create the webhook
    webhook_id = subscribe_to_wallet_webhook(
        # TODO - Append the webhook secret, user id and wallet name
        callback_url=blockcypher_config.get('webhook_callback_url'),
        wallet_name=wallet_name,
        event='unconfirmed-tx',
        api_key=api_key)

    # Store the user address in DB
    UserAddress.add(user.user_id, address, 'XPUB', wallet_name=wallet_name, webhook_id=webhook_id)
