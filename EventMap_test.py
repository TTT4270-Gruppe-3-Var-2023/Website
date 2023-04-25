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
from multiprocessing import Process

MQTT_ADDRESS = "192.168.43.206" #Her må resten av IP-addressen skrives inn
MQTT_USER = "Gruppe3"
MQTT_PASSWORD = "(XWtp·/3gzPylsW"
MQTT_TOPIC_PIRSENSOR = "pir-sensor"
MQTT_TOPIC_ULTRASOUND = "ultrasound"
MQTT_TOPIC_DOPPLERRADAR = "doppler-radar"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_PIRSENSOR)
    client.subscribe(MQTT_TOPIC_ULTRASOUND)
    client.subscribe(MQTT_TOPIC_DOPPLERRADAR)

def on_message(client, userdata, msg):
    print(msg.topic + '  '+ str(msg.payload))
    
 


    

def loop_a():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def loop_b():
    ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        received_data = str(received_data)
        print (float(received_data.replace("b'","").replace("'","")))                   #print received data
        
def loop_c():
    asyncio.run(websocket_main())

if __name__ == '__main__':

    print("Data\n")
    Process(target=loop_a).start()
    Process(target=loop_b).start()
    Process(target=loop_c).start()

def loop_a():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def loop_b():
    ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        received_data = str(received_data)
        print (float(received_data.replace("b'","").replace("'","")))                   #print received data
        
def loop_c():
    asyncio.run(websocket_main())

if __name__ == '__main__':

    print("Data\n")
    Process(target=loop_a).start()
    Process(target=loop_b).start()
    Process(target=loop_c).start()







