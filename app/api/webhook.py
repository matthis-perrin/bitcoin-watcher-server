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

    from_addresses_info = AddressLookup.multi_get(user_id, from_addresses)
    to_addresses_info = AddressLookup.multi_get(user_id, to_addresses)

    amount_spent = 0
    amount_received = 0

    # Look at the oldest address found, if we don't have a lookup for the next 10 addresses, we generate them
    # TODO - Some of those addresses might have a different xpub, we should get the oldest for each xpub
    #        and generate the address lookup for each.
    if len(from_addresses_info) + len(to_addresses_info) > 0:
        oldest = reduce(lambda best, address: address if address.offset > best.offset else best, from_addresses_info + to_addresses_info)
        max = AddressLookup.get_oldest(user_id, oldest.xpub)
        if (oldest.offset > max.offset - 10):
            sub_addresses = []
            indexes = []
            for i in xrange(oldest.offset + 1, oldest.offset + 11):
                sub_address = generate_address_from_xpub(oldest.xpub, i)
                sub_addresses.append(sub_address)
                indexes.append(i)
            AddressLookup.multi_add(user_id, sub_addresses, indexes, oldest.wallet_name, oldest.xpub)

            # Do one more round-trip to the database now that we have more data
            from_addresses_info = AddressLookup.multi_get(user_id, from_addresses)
            to_addresses_info = AddressLookup.multi_get(user_id, to_addresses)


        # Create arrays of addresses owned by the user
        def io_has_address(io, addresses):
            for address in io.get('addresses'):
                if address in addresses:
                    return True
            return False
        from_addresses_owned = [info.address for info in from_addresses_info]
        to_addresses_owned = [info.address for info in to_addresses_info]

        # Filter the inputs and outputs owned by the user
        inputs_owned = filter(lambda input: io_has_address(input, from_addresses_owned), inputs)
        outputs_owned = filter(lambda output: io_has_address(output, to_addresses_owned), outputs)

        # Gather amount spent and received (in satoshi)
        amount_spent = sum([input.get('output_value') for input in inputs_owned])
        amount_received = sum([output.get('value') for output in outputs_owned])
    else:
        # We know nothing about the inputs or outputs, nothing we can do...
        return

    diff = amount_received - amount_spent
    if diff > 0:
        print 'Received {} satoshis'.format(diff)
    elif diff < 0:
        print 'Sent {} satoshis'.format(-diff)
    elif amount_received > 0:
        print 'Sent {} satoshis to yourself'
