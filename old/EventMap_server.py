#!/usr/bin/env python

'''
Websockets server using Pyhton
https://websockets.readthedocs.io/en/stable/howto/quickstart.html
'''

# Imports libraries to run our websockets-server
import asyncio
import websockets
import json 

# SHOULD BE REMOVED ONCE WE NO LONGER USE RANDOM NUMBER GENERATING AND ROUNDS IT TO AN INTEGER!!!
import random
from math import floor

# Prints a statement that can be read in the terminal when the script starts up
print("EventMap_server.py is running")

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
async def broadcast_statuses(pir_stat, ult_stat, dop_stat, uart_stat):
    while True:
        # Subtracts amount of occupied booths from the total to find available booths in a toilet room
        ladies_1_status = 3 - pir_stat.value - ult_stat.value - dop_stat.value

        # Calculates bar queue waiting time based on number of people times average waiting time
        bar_1_wait = uart_stat.value * 3

        # Collects the information that is to be sent in a dictionary
        statuses_dict = {
            "ladies_1": str(ladies_1_status),
            "handicap_1": str(floor(random.randint(0, 1))),
            "mens_1": str(floor(random.randint(0, 3))),
            "ladies_2": str(floor(random.randint(0, 3))),
            "handicap_2": str(floor(random.randint(0, 1))),
            "mens_2": str(floor(random.randint(0, 3))),
            "bar_1": str(bar_1_wait)
        }
        
        # Serializing dictionary to json object
        statuses_json = json.dumps(statuses_dict, indent = 4)
        
        # Sends JSON object to client
        websockets.broadcast(CONNECTIONS, statuses_json)
        
        # Awaits a ranom interval of seconds before repeating cycle
        await asyncio.sleep(random.randint(2, 5))

# Broadscasts on port 5678
async def websocket_main(pir_stat, ult_stat, dop_stat, uart_stat):
    async with websockets.serve(register, "localhost", 5678):
        await broadcast_statuses(pir_stat, ult_stat, dop_stat, uart_stat)

'''
MQTT communication on Raspberry Pi using Pyhton
https://www.engineersgarage.com/raspberry-pi-esp32-esp8266-mqtt-iot/
'''

import serial
from time import sleep
import paho.mqtt.client as mqtt
from multiprocessing import Process, Value, Array

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

def on_message(pir_stat, ult_stat, dop_stat, client, userdata, msg):
    mqtt_payload = str(msg.payload)[2:-1]
    print(msg.topic + '  ' + mqtt_payload)

    if str(msg.topic) == 'pir-sensor':
        pir_stat.value = int(mqtt_payload)
        
        '''
        if int(mqtt_payload) == 1 and pir_stat.value == 0:
            pir_stat.value += 1
        elif int(mqtt_payload) == 0 and pir_stat.value == 1:
            pir_stat.value -= 1
        '''
            
    if str(msg.topic) == 'ultrasound':
        ult_stat.value = int(mqtt_payload)

        '''
        if int(mqtt_payload) == 1 and ult_stat.value == 0:
            ult_stat.value += 1
        elif int(mqtt_payload) == 0 and ult_stat.value == 1:
            ult_stat.value -= 1
        '''
        

    if str(msg.topic) == 'doppler-sensor':
        dop_stat.value = int(mqtt_payload)

        '''
        if int(mqtt_payload) == 1 and dop_stat.value == 0:
            dop_stat.value += 1
        elif int(mqtt_payload) == 0 and dop_stat.value == 1:
            dop_stat.value -= 1
        '''

# Defines the three protocol loops and runs them using multiprocessing-library
def loop_mqtt(pir_stat, ult_stat, dop_stat):
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message(pir_stat, ult_stat, dop_stat)
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    # mqtt_client.loop_forever()

def loop_uart(uart_stat):
    ser = serial.Serial ("/dev/ttyS0", 9600)            #Open port with baud rate
    while True:
        uart_data = ser.read()                 #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()                     #check for remaining byte
        uart_data += ser.read(data_left)
        
        # received_data = str(received_data)
        # received_data = float(received_data.replace("b'","").replace("'","")))                   #print received data
        
        uart_stat.value = float(str(uart_data)[2:-1])

        
def loop_websockets(pir_stat, ult_stat, dop_stat, uart_stat):
    asyncio.run(websocket_main(pir_stat, ult_stat, dop_stat, uart_stat))

if __name__ == '__main__':
    print("Data\n")

    # Defines variables as integers ('i) to be given values from sensors thorugh mqtt and uart, and sent to clients from our websocket server
    pir_stat = Value('i', 0)
    ult_stat = Value('i', 0)
    dop_stat = Value('i', 0)
    uart_stat = Value('i', 0)

    p1 = Process(target=loop_mqtt, args=(pir_stat, ult_stat, dop_stat))
    p2 = Process(target=loop_uart, args=(uart_stat))
    p3 = Process(target=loop_websockets, args=(pir_stat, ult_stat, dop_stat, uart_stat))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

