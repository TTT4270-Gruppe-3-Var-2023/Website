#!/usr/bin/env python

# Importing libraries to use multiprcessing to run mqtt, uart and websockets
import paho.mqtt.client as mqtt                                                 # MQTT
import serial                                                                   # UART
from time import sleep                                                          # UART
import asyncio                                                                  # Websockets
import websockets                                                               # Websockets
import json                                                                     # Websockets
from multiprocessing import Process, Manager                                    # Multiprocessing


# SHOULD BE REMOVED ONCE WE NO LONGER USE RANDOM NUMBER GENERATING AND ROUNDS IT TO AN INTEGER!!!
import random
from math import floor

# Prints a statement that can be read in the terminal when the script starts up
print("EventMap_test_server.py is running")

'''
MQTT and UART communication to Raspberry Pi using Pyhton
https://www.engineersgarage.com/raspberry-pi-esp32-esp8266-mqtt-iot/
'''

MQTT_ADDRESS = "192.168.43.206" # Enter IP-adress here
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

def on_message(statuses_dict, client, userdata, msg):
    print("on_message")

    # mqtt_payload = str(msg.payload)[2:-1]
    # print("mqtt on_message")
    # print(msg.topic + '  ' + mqtt_payload)

    # if str(msg.topic) == 'pir-sensor':
    #     statuses_dict['pir_state'] = int(mqtt_payload)  
    # if str(msg.topic) == 'ultrasound':
    #     statuses_dict['ult_state'] = int(mqtt_payload)
    # if str(msg.topic) == 'doppler-sensor':
    #     statuses_dict['dop_state'] = int(mqtt_payload)
    # else:
    #     print("else\t")
    #     statuses_dict['dop_state'] += 1
    #     print(statuses_dict)

def mqtt_function(statuses_dict):
    print("mqtt")
    while True:
        statuses_dict['pir_state'] = 6
        print('uart_state: ' + str(statuses_dict['uart_state']))

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message(statuses_dict)
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def uart_function(statuses_dict):
    # ser = serial.Serial ("/dev/ttyS0", 9600)            # Open port with baud rate
    print("uart")
    while True:
        statuses_dict['uart_state'] = 5
        print('pir_state: ' + str(statuses_dict['pir_state']))

    #     uart_data = ser.read()                          # Read serial port
    #     sleep(0.03)
    #     data_left = ser.inWaiting()                     # Check for remaining byte
    #     uart_data += ser.read(data_left)                # Print received data
    #     statuses_dict['uart_state'] = float(str(uart_data)[2:-1])
    #     print("uart\t")
    #     print(statuses_dict)
    
'''
Websockets server using Pyhton
https://websockets.readthedocs.io/en/stable/howto/quickstart.html
'''

# Creates an empty set object
CONNECTIONS = set()

# Registers the clients that are connected to the server
async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

# Broadcasts toilet occupancy and bar queue time to the connected clients with a random intervall between 2 and 5 seconds
async def broadcast_statuses(statuses_dict):
    while True:
        # Subtracts amount of occupied booths from the total to find available booths in a toilet room
        ladies_1_status = 3 - statuses_dict['pir_state'] - statuses_dict['ult_state'] - statuses_dict['dop_state']
        # Calculates bar queue waiting time based on number of people times average waiting time
        bar_1_wait = statuses_dict['uart_state'] * 3

        # Collects the information that is to be sent in a dictionary
        display_dict = {
            "ladies_1": str(ladies_1_status),
            "handicap_1": str(floor(random.randint(0, 1))),
            "mens_1": str(floor(random.randint(0, 3))),
            "ladies_2": str(floor(random.randint(0, 3))),
            "handicap_2": str(floor(random.randint(0, 1))),
            "mens_2": str(floor(random.randint(0, 3))),
            "bar_1": str(bar_1_wait)
        }
        
        # Serializing dictionary to json object
        statuses_json = json.dumps(display_dict, indent = 4)
        
        # Sends JSON object to client
        websockets.broadcast(CONNECTIONS, statuses_json)
        
        # Awaits a ranom interval of seconds before repeating cycle
        await asyncio.sleep(random.randint(2, 5))

        print("broadcast")
        print(display_dict)

# Broadscasts on port 5678
async def websocket_main(statuses_dict):
    async with websockets.serve(register, "localhost", 5678):
        await broadcast_statuses(statuses_dict)

def websockets_function(statuses_dict):
    print("websockets")
    print(statuses_dict)
    asyncio.run(websocket_main(statuses_dict))

if __name__ == '__main__':
    print("main is running")
    
    with Manager() as manager:
        statuses_dict = manager.dict()
        statuses_dict['pir_state'] = 0
        statuses_dict['ult_state'] = 0
        statuses_dict['dop_state'] = 0
        statuses_dict['uart_state'] = 0.0
        print(statuses_dict)

        p1 = Process(target=mqtt_function, args=(statuses_dict,))
        p2 = Process(target=uart_function, args=(statuses_dict,))
        p3 = Process(target=websockets_function, args=(statuses_dict,))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()
