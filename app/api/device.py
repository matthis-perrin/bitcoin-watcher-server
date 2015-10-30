from app.api.utils import api
from app.db.user_device import UserDevice
from app.exception import MyBitsException


@api(enforce_user=True)
def register(context, request, api_version, user,
             platform=None, system_version=None, app_version=None, push_token=None):

    if not platform: raise MyBitsException('Parameter `platform` missing')
    if not system_version: raise MyBitsException('Parameter `system_version` missing')
    if not app_version: raise MyBitsException('Parameter `app_version` missing')
    if not push_token: raise MyBitsException('Parameter `push_token` missing')

    device_id = UserDevice.create(user.user_id, platform, system_version, app_version, push_token)
    return dict(device_id=device_id)
