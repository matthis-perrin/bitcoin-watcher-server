from functools import partial

import app.api.user as user
import app.api.device as device


def handle_404(request):
    return dict(error='Unknown route')


def wire_route(config, path=None, handler=None, renderer='json', request_method='POST'):
    route_name = path
    config.add_route(route_name, path, request_method=request_method)
    config.add_view(handler, route_name=route_name, renderer=renderer)


def wire_routes(config):
    wire_route(config, path='/user/register', handler=user.register)
    wire_route(config, path='/user/{user_id}/device/register', handler=device.register)

    config.add_view(handle_404, renderer='json', context='pyramid.httpexceptions.HTTPNotFound')
