from random import random

from app.db.mysql import MySQL


class User:

    def __init__(self, *args):
        self.user_id, self.creation_time, self.last_seen = args

    @staticmethod
    def get(user_id):
        res = MySQL.run('SELECT * FROM user WHERE user_id = {}'.format(user_id))
        return User(*res)

    @staticmethod
    def create():
        """
        Create a new user in db.

        Returns the `user_id` of the newly created user
        """
        user_id = int(random() * 4294967295)
        res = MySQL.run('INSERT INTO user (user_id) VALUES ({})'.format(user_id))
        return user_id
