from MySQLdb import IntegrityError

from app.db.core.mysql import MySQL
from app.exception import MyBitsException


class UserAddress:

    def __init__(self, *args):
        (self.user_id,
         self.address,         # Text representation of a bitcoin address
         self.address_type,    # Type of address (plain text for now) TODO - Make that an enum
         self.creation_time,   # When the address got linked to the user
         ) = args

    @staticmethod
    def get_by_address(user_id, address):
        """
        Returns the address `address` linked to the user `user_id`.
        """
        res = MySQL.run('SELECT * FROM user_address WHERE user_id = {} AND address = {}'.format(user_id, address))
        if len(res) == 0:
            raise MyBitsException('Address {} for user {} not found'.format(address, user_id))
        return UserAddress(*res[0])

    @staticmethod
    def get_all(user_id=None):
        """
        Returns all the addresses linked to the user `user_id`.
        """
        query = 'SELECT * FROM user_address'
        if user_id:
            query += ' WHERE user_id = {}'.format(user_id)
        res = MySQL.run(query)
        return [UserAddress(*address_data) for address_data in res]

    @staticmethod
    def add(user_id, address, address_type):
        """
        Add the address `address` for the user `user_id`.
        """
        query = '''
          INSERT INTO user_address (user_id, address, address_type)
          VALUES ({}, '{}', '{}')
        '''.format(user_id, address, address_type)
        try:
            MySQL.run(query)
        except IntegrityError as e:
            raise MyBitsException('Address {} is already linked to user {}'.format(address, user_id))
            print e.message

