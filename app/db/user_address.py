from random import random

from app.db.core.mysql import MySQL
from app.exception import MyBitsException


class UserAddress:

    def __init__(self, *args):
        (self.user_id,
         self.address,         # Text representation of a bitcoin address
         self.type,            # Type of address (plain text for now) TODO - Make that an enum
         self.wallet_name,     # Name of the wallet on blockcypher
         self.webhook_id,      # Id of the webhook on blockcypher
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
    def get_by_wallet_name(wallet_name):
        """
        Returns the address registered to the wallet `wallet_name` on BlockCypher..
        """
        res = MySQL.run("SELECT * FROM user_address WHERE wallet_name = '{}'".format(wallet_name))
        if len(res) == 0:
            raise MyBitsException('Address with wallet {} not found'.format(wallet_name))
        return UserAddress(*res[0])

    @staticmethod
    def get_all(user_id):
        """
        Returns all the addresses linked to the user `user_id`.
        """
        res = MySQL.run('SELECT * FROM user_device WHERE user_id = {}'.format(user_id))
        return [UserAddress(*address_data) for address_data in res]

    @staticmethod
    def add(user_id, address, address_type, wallet_name, webhook_id):
        """
        Add the address `address` for the user `user_id`.
        """
        device_id = int(random() * (2 ** 32 - 1))
        query = '''
          INSERT INTO user_address (user_id, address, address_type, wallet_name, webhook_id)
          VALUES ({}, '{}', '{}', '{}', '{}')
        '''.format(user_id, address, address_type, wallet_name, webhook_id)
        MySQL.run(query)

