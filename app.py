from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



from sales.models import db_session, User
from sales.api.queries import schema

from flask_sockets import Sockets

from graphql_ws.gevent import GeventSubscriptionServer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Admin', template_mode='bootstrap3')

cors = CORS(app, resources={r"*": {"origins": "*"}})
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



admin.add_view(ModelView(User, db_session))

@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return []


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


