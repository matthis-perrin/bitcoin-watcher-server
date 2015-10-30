from random import random

from app.db.core.mysql import MySQL
from app.exception import MyBitsException


class UserDevice:

    def __init__(self, *args):
        (self.device_id,       # Device id generated the first time the device makes a request to the server
         self.user_id,
         self.platform,        # Device model (eg 'iPhone8,2')
         self.system_version,  # iOS version (eg '8.1')
         self.app_version,     # Version of the Bitcoin Watcher app (eg '0.0.1')
         self.push_token,      # Device token that allows the server to send push notification to the device
         self.creation_time,   # First time the user opens the app on a device
         self.last_seen,       # Last time the user opened the app on a device
         ) = args

    @staticmethod
    def get(device_id):
        """
        Returns the device `device_id`.
        """
        res = MySQL.run('SELECT * FROM user_device WHERE device_id = {}'.format(device_id))
        if len(res) == 0:
            raise MyBitsException('Device {} not found'.format(device_id))
        return UserDevice(*res[0])

    @staticmethod
    def get_all(user_id):
        """
        Returns all the devices linked to the user `user_id`.
        """
        res = MySQL.run('SELECT * FROM user_device WHERE user_id = {}'.format(user_id))
        return [UserDevice(*device_data) for device_data in res]

    @staticmethod
    def create(user_id, platform, system_version, app_version, push_token):
        """
        Create a new device for the user `user_id`.
        Returns the `device_id` of the newly created user device.
        """
        device_id = int(random() * (2 ** 32 - 1))
        query = '''
          INSERT INTO user_device (device_id, user_id, platform, system_version, app_version, push_token, last_seen)
          VALUES ({}, {}, '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP)
        '''.format(device_id, user_id, platform, system_version, app_version, push_token)
        MySQL.run(query)
        return device_id
