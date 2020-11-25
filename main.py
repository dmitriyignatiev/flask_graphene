import asyncio
import json
from datetime import datetime
from flask_socketio import SocketIO, emit

import graphene
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from memory_profiler import memory_usage

from sales.api.mutations import myMutation
from sales.api.queries import Query
from sales.api.subscriptions import Subscription
from sales.models import db_session
from flask_sockets import Sockets
from graphql_ws.gevent import GeventSubscriptionServer


app = Flask(__name__)
sockets = Sockets(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


app.debug = True


schema = graphene.Schema(
                         query=Query,
                         mutation=myMutation,
                         subscription=Subscription
                         )


subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'

@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return []


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True

    )
)

socketio = SocketIO(app)

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


async def check_memory():
    memory = []
    while True:
        memory.append(memory_usage()[0])
        print('check_memory_usage date_time: {} memory: {}'.format(datetime.now().isoformat(), memory_usage()))
        await asyncio.sleep(5)
        with open('test.json', 'w') as file:
            file.write(json.dumps(memory))


if __name__ == '__main__':

    from geventwebsocket import WebSocketServer
    server = WebSocketServer(('', 5000), app)
    print('Serving at host 0.0.0.0:5000...\n')
    print('check_memory_usage date_time: {} memory: {}'.format(datetime.now().isoformat(), memory_usage()))
    socketio.run(app)
    server.serve_forever()


