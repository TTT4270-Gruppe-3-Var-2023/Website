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
        
        print(statuses_dict)
        print("broad\n")

# Broadscasts on port 5678
async def websocket_main():
    async with websockets.serve(register, "localhost", 5678):
        await broadcast_statuses()

'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''

import serial
from time import sleep
import paho.mqtt.client as mqtt
from multiprocessing import Process, Lock, Value

MQTT_ADDRESS = "192.168.**.***" #Her må resten av IP-addressen skrives inn
MQTT_USER = "***"
MQTT_PASSWORD = "***"
MQTT_TOPIC_PIRSENSOR = "pir-sensor"
MQTT_TOPIC_ULTRASOUND = "ultrasound"
MQTT_TOPIC_DOPPLERRADAR = "doppler-radar"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_PIRSENSOR)
    client.subscribe(MQTT_TOPIC_ULTRASOUND)
    client.subscribe(MQTT_TOPIC_DOPPLERRADAR)

def on_message(client, userdata, msg):
    print(msg.topic + '  '+ str(msg.payload)[2:-1])

def loop_a(pir_state, lock):
    print("a\n")
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def loop_b():
    print("b\n")
    ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
    while True:
       received_data = ser.read()              #read serial port
       sleep(0.03)
       data_left = ser.inWaiting()             #check for remaining byte
       received_data += ser.read(data_left)
       received_data = str(received_data)
       print (float(received_data.replace("b'","").replace("'","")))                   #print received data

def loop_c():
    print("c\n")
    asyncio.run(websocket_main())

if __name__ == '__main__':
    print("Data\n")

    pir_state = Value('i', 0)
    lock = Lock()

    p_1 = Process(target=loop_a, args=(pir_state, lock))
    p_1.start()

    p_2 = Process(target=loop_b)
    p_2.start()

    p_3 = Process(target=loop_c)
    p_3.start()
    
    p_1.join()
    p_2.join()
    p_3.join()

    print('pir_state: ' + pir_state.value)









