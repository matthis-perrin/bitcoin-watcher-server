from app.config import Config

from app.exception import MyBitsException
from app.db.address_lookup import AddressLookup
from app.db.user_address import UserAddress
from app.bitcoin.util import generate_address_from_xpub


blockcypher_config = Config.get('blockcypher')
webhook_secret = blockcypher_config.get('webhook_secret')

def webhook_receive(context, request):
    received_secret = request.matchdict['webhook_secret']
    user_id = request.matchdict['user_id']
    wallet_name = request.matchdict['wallet_name']
    if received_secret != webhook_secret:
        raise MyBitsException('Invalid webhook secret')

    user_address = UserAddress.get_by_wallet_name(wallet_name)
    xpub = user_address.address

    data = request.json_body
    inputs = data.get('inputs')
    outputs = data.get('outputs')

    from_addresses = reduce(lambda all_addresses, input: all_addresses + input.get('addresses'), inputs, [])
    to_addresses = reduce(lambda all_addresses, output: all_addresses + output.get('addresses'), outputs, [])

    # TODO - This is slow and flaky... Need something else
    for i in xrange(100):
        next_address = generate_address_from_xpub(xpub, index=i)
        if next_address in from_addresses:
            receive = False
            break
        elif next_address in to_addresses:
            receive = True
            break

    addresses_info = AddressLookup.multi_get(user_id, from_addresses + to_addresses)
    print addresses_info

    # if receive is None:
    #     return
    #
    # addresses = from_addresses if receive else to_addresses
    # index = addresses.index(next_address)
    # # amount = addresses[index].get('')
