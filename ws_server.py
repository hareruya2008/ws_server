#!/usr/bin/env python

# WS server example that synchronizes state across clients
#收到什么发什么给所有连接端
import asyncio
import json
import websockets

USERS = set()

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])
        
async def notify_all(message):
    if USERS:       # asyncio.wait doesn't accept an empty list
        #message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])
        
async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    
    await register(websocket)
    try:
        async for message in websocket:
            await notify_all(message)
           
    finally:
        await unregister(websocket)
        
start_server = websockets.serve(counter, 'localhost', 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()