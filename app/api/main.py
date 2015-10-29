import app.api.user as user

def wire_route(config, path=None, handler=None, renderer='json'):
    route_name = path
    config.add_route(route_name, path)
    config.add_view(handler, route_name=route_name, renderer=renderer)

def wire_routes(config):
    wire_route(config, path='/user/register', handler=user.register)
