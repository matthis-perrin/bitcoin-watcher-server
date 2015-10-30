import traceback

from app.db.user import User
from app.exception import MyBitsException


def api(enforce_user=False):
    def api_decorator(func):
        def func_wrapper(context, request):
            additional_params = []
            query_params = request.matchdict
            try:
                json_body = {}
                if enforce_user:
                    if 'user_id' not in query_params:
                        return dict(error='Expected `user_id` in query')
                    additional_params.append(User.get(query_params['user_id']))
                    try:
                        json_body = request.json_body
                    except Exception:
                        pass
                return func(context, request, *additional_params, **json_body)
            except MyBitsException as e:
                return dict(error=e.message)
            except Exception as e:
                traceback.print_exc()
                print str(e)
                return dict(error='Unexcepted error')

        return func_wrapper
    return api_decorator
