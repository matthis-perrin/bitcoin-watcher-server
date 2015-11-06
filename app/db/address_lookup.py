from app.db.core.mysql import MySQL


class AddressLookup:

    def __init__(self, *args):
        (self.address,        # The bitcoin address
         self.user_id,        # The id of the user that owns this address
         self.xpub,           # The actual xpub the bitcoin address is derived from
         self.offset,         # The index of the address in the xpub chain
         self.creation_time,  # When the address lookup got created
         ) = args

    @staticmethod
    def get(user_id, address):
        """
        Returns all the info of where the address is coming from (restricted to a specific `user_id`)
        """
        res = MySQL.run('''
          SELECT address, user_id, xpub, offset, creation_time FROM address_lookup
          WHERE user_id = {} AND address = {}'''.format(user_id, address))
        if len(res) == 0:
            return None
        return AddressLookup(*res[0])

    @staticmethod
    def get_oldest(user_id, xpub):
        """
        Returns the info of the oldest address for a specific `user_id` and `xpub`
        """
        res = MySQL.run('''
          SELECT address, user_id, xpub, offset, creation_time FROM address_lookup
          WHERE user_id = {} AND xpub = '{}' ORDER BY offset DESC LIMIT 1'''.format(user_id, xpub))
        if len(res) == 0:
            return None
        return AddressLookup(*res[0])


    @staticmethod
    def multi_get(user_id, addresses):
        """
        Returns the info of all the `addresses` that we have in the lookup table (restricted to a specific `user_id`)
        """
        addresses = "', '".join(addresses)
        res = MySQL.run('''
          SELECT address, user_id, xpub, offset, creation_time FROM address_lookup
          WHERE user_id = {} AND address IN ('{}')'''.format(user_id, addresses))
        return [AddressLookup(*address_info) for address_info in res]

    @staticmethod
    def add(user_id, address, xpub):
        """
        Add the address info to the lookup table.
        """
        query = '''
          INSERT INTO address_lookup (user_id, address, xpub)
          VALUES ({}, '{}', '{}', '{}')
        '''.format(user_id, address, xpub)
        MySQL.run(query)

    @staticmethod
    def multi_add(user_id, addresses, offsets, xpub):
        """
        Add multiple addresses info to the lookup table.
        """
        query = '''
          INSERT INTO address_lookup (user_id, address, xpub, offset)
          VALUES
        '''
        values = []
        for i in xrange(0, len(addresses)):
            address = addresses[i]
            offset = offsets[i]
            values.append("({}, '{}', '{}', {})".format(user_id, address, xpub, offset))
        query += ", ".join(values)
        MySQL.run(query)

