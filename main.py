from blockcypher import (
    create_hd_wallet,
    delete_wallet,
    list_wallet_names,
    list_webhooks,
    subscribe_to_wallet_webhook,
    unsubscribe_from_webhook
)
from pyramid.config import Configurator
from wsgiref.simple_server import make_server

from app.api.core.routes import wire_routes
from app.config import Config
from app.db.user_address import UserAddress


print 'Listing wallets and webhooks on BlockCypher and in DB...'

# List all the wallets and webhooks on BlockCypher
blockcypher_config = Config.get('blockcypher')
blockcypher_api_key = blockcypher_config .get('api_key')
wallets = list_wallet_names(blockcypher_api_key)['wallet_names']
print '  {} wallets found on BlockCypher'.format(len(wallets))
webhooks = list_webhooks(blockcypher_api_key)
print '  {} webhooks found on BlockCypher'.format(len(webhooks))

# List all the wallets in DB
user_addresses = UserAddress.get_all()
print '  {} wallets found in DB'.format(len(user_addresses))

# Remove from BlockCypher the wallet and webhooks that are not in DB
print 'Deleting extra wallets and webhooks on BlockCypher'
deleted_wallets = 0
deleted_webhooks = 0
user_addresses_as_wallet_names = [user_address.wallet_name for user_address in user_addresses]
for wallet in wallets:
    if wallet not in user_addresses_as_wallet_names:
        delete_wallet(wallet, blockcypher_api_key, is_hd_wallet=True)
        deleted_wallets += 1
print '  {} wallets deleted'.format(deleted_wallets)
user_addresses_as_webhook_ids = [user_address.webhook_id for user_address in user_addresses]
for webhook in webhooks:
    if webhook not in user_addresses_as_webhook_ids:
        try:
            unsubscribe_from_webhook(webhook, blockcypher_api_key)
            deleted_wallets += 1
        except Exception as e:
            print "  Couldn't unsubscribe from webhook {}".format(webhook)
print '  {} webhooks deleted'.format(deleted_wallets)

# Add to BlockCypher the wallet and webhooks that are missing but are in DB
print 'Adding missing wallets and webhooks on BlockCypher'
added_wallets = 0
added_webhook = 0
for user_address in user_addresses:
    if user_address.wallet_name not in wallets:
        create_hd_wallet(user_address.wallet_name, user_address.address, blockcypher_api_key)
        added_wallets += 1
    if user_address.webhook_id not in webhooks:
        subscribe_to_wallet_webhook(callback_url=blockcypher_config.get('webhook_callback_url'),
                                    wallet_name=user_address.wallet_name,
                                    event='unconfirmed-tx',
                                    api_key=blockcypher_api_key)
        added_webhook += 1
print '  {} wallets added'.format(added_wallets)
print '  {} webhooks added'.format(added_webhook)

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
