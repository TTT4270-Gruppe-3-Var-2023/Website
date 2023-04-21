#!/usr/bin/env python

# Imports libraries to be used
import asyncio
import random
import websockets
import json 
from math import floor


# Prints a statement that can be read in the terminal when the script is running
print("EventMap.py is running")

# Creates an empty set object
CONNECTIONS = set()

# Registers the clients that are connected to the server
async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

# Saves a random integer between 1 and 5 in the variable "status" and broadcasts it to the connected clients with a random intervall between 2 and 5 seconds
async def broadcast_statuses():
    while True:
        statuses_dict = {
            "ladies_1": str(floor(random.randint(0, 5))),
            "handicap_1": str(floor(random.randint(0, 1))),
            "mens_1": str(floor(random.randint(0, 5))),
            "ladies_2": str(floor(random.randint(0, 5))),
            "handicap_2": str(floor(random.randint(0, 1))),
            "mens_2": str(floor(random.randint(0, 5)))
        }
        
        # Serializing json  
        statuses_json = json.dumps(statuses_dict, indent = 4)
        
        # Sends JSON object 
        websockets.broadcast(CONNECTIONS, statuses_json)
        await asyncio.sleep(random.randint(2, 5))

# Broadscasts on port 5678
async def main():
    async with websockets.serve(register, "localhost", 5678):
        await broadcast_statuses()

# runs the main function
if __name__ == "__main__":
    asyncio.run(main())