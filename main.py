from app.db.user import User
from app.db.user_device import UserDevice

def print_user(user):
    print user.user_id, user.creation_time
    print '\n'

def print_device(device):
    print (device.user_id, device.device_id, device.platform, device.system_version, device.app_version,
           device.app_version, device.creation_time, device.last_seen)
    print '\n'

user_id = User.create()
user = User.get(user_id)
print_user(user)

device_id_1 = UserDevice.create(user_id, "platform1", "system_version1", "app_version1", 'push_token1')
device_id_2 = UserDevice.create(user_id, "platform2", "system_version2", "app_version2", 'push_token2')

device1 = UserDevice.get(device_id_1)
device2 = UserDevice.get(device_id_1)

print_device(device1)
print_device(device2)

for device in user.get_devices():
    print_device(device)
