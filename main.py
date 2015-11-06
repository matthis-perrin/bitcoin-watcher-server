from pyramid.config import Configurator
from wsgiref.simple_server import make_server

from app.api.core.routes import wire_routes
from app.config import Config


# Setup the api routes
config = Configurator()
wire_routes(config)
config.scan()

# Start the server
api_config = Config.get('api')
host = api_config.get('host')
port = api_config.get('port')
app = config.make_wsgi_app()
server = make_server(host, port, app)
print 'Started API on {}:{}'.format(host, port)
server.serve_forever()
