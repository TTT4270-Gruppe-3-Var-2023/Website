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

##!/usr/bin/env python

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

# Saves a random integer between 1 and 3 in the dictionary to be displayed and broadcasts it to the connected clients with a random intervall between 2 and 5 seconds
async def broadcast_statuses(statuses_dict):
    print("broadcasting") 
    
    if statuses_dict['ult_state'] < 10:
        ult_var = 1
    else:
        ult_var = 0

    ladies_1_count = 3 - statuses_dict['pir_state'] - ult_var - statuses_dict['dop_state']

    bar_1_wait = statuses_dict['uart_state'] * 3 # Number of people in queue times average wait time in minutes

    while True:
        display_dict = {
            "ladies_1": str(ladies_1_count),
            "handicap_1": str(floor(random.randint(0, 1))),
            "mens_1": str(floor(random.randint(0, 3))),
            "ladies_2": str(floor(random.randint(0, 3))),
            "handicap_2": str(floor(random.randint(0, 1))),
            "mens_2": str(floor(random.randint(0, 3))),
            "bar_1": str(bar_1_wait)
        }
        
        # Serializing json  
        statuses_json = json.dumps(display_dict, indent = 4)
        
        # Sends JSON object 
        websockets.broadcast(CONNECTIONS, statuses_json)
        await asyncio.sleep(random.randint(2, 5))
        
        print('display_dict')
        print(display_dict)

# Broadscasts on port 5678
async def websocket_main(statuses_dict):
    async with websockets.serve(register, "localhost", 5678):
        await broadcast_statuses(statuses_dict)

'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''

# import serial
from time import sleep
import paho.mqtt.client as mqtt
from multiprocessing import Process, Manager

MQTT_ADDRESS = "192.168.**.***" #Her må resten av IP-addressen skrives inn
MQTT_USER = "Gruppe3"
MQTT_PASSWORD = "***"
MQTT_TOPIC_PIRSENSOR = "pir-sensor"
MQTT_TOPIC_ULTRASOUND = "ultrasound"
MQTT_TOPIC_DOPPLERRADAR = "doppler-radar"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_PIRSENSOR)
    client.subscribe(MQTT_TOPIC_ULTRASOUND)
    client.subscribe(MQTT_TOPIC_DOPPLERRADAR)

def on_message(statuses_dict, client, userdata, msg):    
    print("mqtt on_message")
    
    topic = str(msg.topic)
    payload = str(msg.payload)[2:-1]

    if topic == 'pir-sensor':
        statuses_dict['pir_state'] = int(payload)
    if topic == 'ult-sensor':
        statuses_dict['ult_state'] = int(payload)
    if topic == 'dop-sensor':
        statuses_dict['dop_state'] = int(payload)

    print(topic + ' ' + payload)    

def loop_a(statuses_dict):
    print('loop a is running (mqtt)')
    print(statuses_dict)

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message(statuses_dict)
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def loop_b(statuses_dict):
    print('loop b is running (uart)')
    print(statuses_dict)
    ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
    while True:
       received_data = ser.read()              #read serial port
       sleep(0.03)
       data_left = ser.inWaiting()             #check for remaining byte
       received_data += ser.read(data_left)
       statuses_dict['uart_state'] = float(str(received_data)[2:-1])
       
       print('uart_state: ')
       print(statuses_dict['uart_state'])                   #print received data

def loop_c(statuses_dict):
    print('loop c is running (websockets)')
    print(statuses_dict)
    asyncio.run(websocket_main(statuses_dict))

if __name__ == '__main__':
    print('main is running')
    
    with Manager() as manager:
        statuses_dict = manager.dict()
        statuses_dict['pir_state'] = 0
        statuses_dict['ult_state'] = 0
        statuses_dict['dop_state'] = 0
        statuses_dict['uart_state'] = 0.0
        print(statuses_dict)

        p_1 = Process(target=loop_a, args=(statuses_dict,))
        p_2 = Process(target=loop_b, args=(statuses_dict,))
        p_3 = Process(target=loop_c, args=(statuses_dict,))
        
        p_1.start()
        p_2.start()
        p_3.start()
        
        p_1.join()
        p_2.join()
        p_3.join()









