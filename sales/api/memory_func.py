import asyncio
import json

import websockets


async def start(i):
    # uri = "ws://localhost:8384/subscriptions"
    # uri = "ws://devel.centr.m:8384/subscriptions"
    uri = "ws://localhost:5000/subscriptions"
    # uri = 'ws://localhost:8000/feed'
    # uri = 'ws://localhost:8768'
    # uri = 'ws://localhost:5000/echo'
    # uri = 'ws://localhost:8000/save_photo'
    # file = open('/home/gdeon/Изображения/14846831769190.png', 'rb')
    # file = file.read()
    async with websockets.connect(uri) as websocket:
        # my_dict = dict(id=1, type="start", payload=file)
        # my_dict = dict(id=1, type="start", payload={
        #     "query": 'subscription{laggedTask{ infrastructureobjectId infraName expiredCount atRisk}}',
        #     "variables": {}
        # })
        my_dict = dict(id=1, type="start", payload={
            "query": 'subscription{countSeconds(upTo:5) }',
            "variables": {}
        })
        # my_dict = dict(id=1, type="start", payload={
        #     "query": "subscription{countSeconds(upTo:5)}",
        #     "variables": {}
        # })
        await websocket.send(json.dumps(my_dict))
        # await websocket.send(file)
        while True:
            # await asyncio.sleep(0.1)
            greeting = await websocket.recv()
            print(i, greeting)
        return


async def start_tasks():
    for i in range(1):
        # asyncio.ensure_future(start(i))
    # await asyncio.sleep(50)
        await asyncio.gather(
            *[start(i) for i in range(1000)]
        )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_tasks())