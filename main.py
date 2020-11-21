from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from sales.models import db_session
from sales.api.queries import schema

from flask_sockets import Sockets
import graphql_ws
from graphql_ws.gevent import GeventSubscriptionServer



app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True
sockets = Sockets(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface


    )
)

subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'

@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return []


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    from geventwebsocket import WebSocketServer
    server = WebSocketServer(('', 5000), app)
    print('Serving at host 0.0.0.0:5000...\n')
    server.serve_forever()
