from app import app

if __name__ == "__main__":
    from geventwebsocket import WebSocketServer

    server = WebSocketServer(('', 5002), app)
    print('Serving at host 0.0.0.0:5002...\n')
    server.serve_forever()