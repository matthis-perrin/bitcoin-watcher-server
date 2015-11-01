from blockcypher import subscribe_to_address_webhook

from app.config import Config
from app.api.core.utils import api
from app.db.user_address import UserAddress
from app.exception import MyBitsException


blockcypher_config = Config.get('blockcypher')

@api(enforce_user=True)
def add(context, request, api_version, user,
        address=None):

    if not address:
        raise MyBitsException('Parameter `address` missing')

    webhook_id = subscribe_to_address_webhook(
        callback_url=blockcypher_config.get('webhook_callback_url'),
        subscription_address=address,
        event='unconfirmed-tx',
        api_key=blockcypher_config.get('api_key'))
    UserAddress.add(user.user_id, address, 'XPUB', webhook_id=webhook_id)
