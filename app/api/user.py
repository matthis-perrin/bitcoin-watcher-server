from app.api.utils import api
from app.db.user import User


@api()
def register(context, request, api_version):
    user_id = User.create()
    return dict(user_id=user_id)
