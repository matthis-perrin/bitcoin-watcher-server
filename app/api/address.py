from random import random

from blockcypher import create_hd_wallet
from blockcypher import subscribe_to_wallet_webhook

from app.config import Config
from app.api.core.utils import api
from app.db.user_address import UserAddress
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

    # Create the webhook
    webhook_id = subscribe_to_wallet_webhook(
        callback_url=blockcypher_config.get('webhook_callback_url'),
        wallet_name=wallet_name,
        event='unconfirmed-tx',
        api_key=blockcypher_config.get('api_key'))

    # Store the user address in DB
    UserAddress.add(user.user_id, address, 'XPUB', wallet_name=wallet_name, webhook_id=webhook_id)
