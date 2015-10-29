from random import random

from app.db.mysql import MySQL
from app.db.user_device import UserDevice


class User:

    def __init__(self, *args):
        (self.user_id,        # User id generated the first time the user make a request to the server
         self.creation_time,  # First time the user used the app
         ) = args

    @staticmethod
    def get(user_id):
        """
        Returns the user from the database with `user_id`
        """
        res = MySQL.run('SELECT * FROM user WHERE user_id = {}'.format(user_id))
        return User(*res[0])

    def get_devices(self):
        """
        Returns all the devices linked to the user with `user_id`
        """
        return UserDevice.get_all(self.user_id)

    @staticmethod
    def create():
        """
        Create a new user in db.
        Returns the `user_id` of the newly created user
        """
        user_id = int(random() * (2**32 - 1))
        MySQL.run('INSERT INTO user (user_id) VALUES ({})'.format(user_id))
        return user_id
