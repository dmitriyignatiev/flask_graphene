from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from sales.models import db_session
from sales.api.queries import schema

from flask_sockets import Sockets
from graphql_subscriptions import (
    SubscriptionManager,
    RedisPubsub,
    SubscriptionServer
)

app = Flask(__name__)
sockets = Sockets(app)
pubsub = RedisPubsub()

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface


    )
)
subscription_mgr = SubscriptionManager(schema, pubsub)

@sockets.route('/socket')
def socket_channel(websocket):
    subscription_server = SubscriptionServer(subscription_mgr, websocket)
    subscription_server.handle()
    return []

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    from geventwebsocket import WebSocketServer
    server = WebSocketServer(('', 5000), app)
    print('Serving at host 0.0.0.0:5000...\n')
    server.serve_forever()
    # app.run()