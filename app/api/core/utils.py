import traceback

from app.db.user import User
from app.exception import MyBitsException

ALLOWED_API_VERSIONS = [1]

def api(enforce_user=False):
    def api_decorator(func):
        def func_wrapper(context, request):
            additional_params = []
            query_params = request.matchdict
            # Extract the API version
            try:
                api_version = int(query_params['api_version'][1:])
                if api_version not in ALLOWED_API_VERSIONS:
                    return dict(error='Invalid api version')
                additional_params.append(api_version)
            except Exception:
                return dict(error='Invalid api version')
            try:
                json_body = {}
                # Grab the user if needed
                if enforce_user:
                    if 'user_id' not in query_params:
                        return dict(error='Expected `user_id` in query')
                    additional_params.append(User.get(query_params['user_id']))
                    try:
                        json_body = request.json_body
                    except Exception:
                        pass
                res = func(context, request, *additional_params, **json_body)
                return res or {}
            # Catch our exceptions
            except MyBitsException as e:
                return dict(error=e.message)
            # Catch any other exceptions
            except Exception as e:
                traceback.print_exc()
                print str(e)
                return dict(error='Unexpected error')

        return func_wrapper
    return api_decorator
