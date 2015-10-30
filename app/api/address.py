from app.api.core.utils import api
from app.db.user_address import UserAddress
from app.exception import MyBitsException


@api(enforce_user=True)
def add(context, request, api_version, user,
        address=None):

    if not address: raise MyBitsException('Parameter `address` missing')

    UserAddress.add(user.user_id, address, 'XPUB')

