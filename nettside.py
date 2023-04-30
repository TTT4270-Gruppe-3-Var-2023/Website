# Prints a statement that can be read in the terminal when the script is running
print("EventMap.py is running")


# Creates an empty set object
CONNECTIONS = set()

##!/usr/bin/env python


# Importing libraries to use multiprcessing to run mqtt, uart and websockets
import paho.mqtt.client as mqtt                                                 # MQTT
import serial                                                                   # UART
from time import sleep                                                          # UART
import asyncio                                                                  # Websockets
import websockets                                                               # Websockets
import json                                                                     # Websockets
from multiprocessing import Process, Manager                                    # Multiprocessing



#Import libraries to simulate data
from math import floor
import random


# Creates an empty set object
CONNECTIONS = set()
# Prints a statement that can be read in the terminal when the script is running
print("EventMap.py is running")

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
    
    while True:

        if statuses_dict['ult_state'] < 10:
            print(statuses_dict['ult_state'])
            ult_var = 1
        else:
            ult_var = 0

        print("ult:"+ str(ult_var))
        ladies_1_count = 3 - int(statuses_dict['pir_state']) - ult_var - int(statuses_dict['dop_state'])
        print(f"tot: {ladies_1_count}")
        
        bar_1_wait = floor(float(statuses_dict['uart_state']) * 3) # Number of people in queue times average wait time in minutes

        display_dict = {
            "mens_0": str(floor(random.randint(0, 3))),
            "mens_1": str(floor(random.randint(0, 3))),
            "mens_2": str(floor(random.randint(0, 3))),
            "mens_3": str(floor(random.randint(0, 3))),
            "mens_4": str(floor(random.randint(0, 3))),
            "mens_5": str(floor(random.randint(0, 3))),
            "mens_6": str(floor(random.randint(0, 3))),
            
            "ladies_0": str(ladies_1_count),
            "ladies_1": str(floor(random.randint(0, 3))),
            "ladies_2": str(floor(random.randint(0, 3))),
            "ladies_3": str(floor(random.randint(0, 3))),
            "ladies_4": str(floor(random.randint(0, 3))),
            "ladies_5": str(floor(random.randint(0, 3))),
            "ladies_6": str(floor(random.randint(0, 3))),
            
            "handicap_0": str(floor(random.randint(0, 1))),
            "handicap_1": str(floor(random.randint(0, 1))),
            "handicap_2": str(floor(random.randint(0, 1))),
            "handicap_3": str(floor(random.randint(0, 1))),
            "handicap_4": str(floor(random.randint(0, 1))),
            "handicap_5": str(floor(random.randint(0, 1))),
            "handicap_6": str(floor(random.randint(0, 1))),
            
            "bar_0": str(bar_1_wait),
            "bar_1": str(floor(random.randint(1, 8))),
            "bar_2": str(floor(random.randint(2, 10))),
            "bar_3": str(floor(random.randint(3, 13))),
            "bar_4": str(floor(random.randint(4, 15)))
        }
        
        # print(display_dict)

        # Serializing json  
        statuses_json = json.dumps(display_dict, indent = 4)
        
        # Sends JSON object 
        websockets.broadcast(CONNECTIONS, statuses_json)
        await asyncio.sleep(random.randint(2, 5))
        
        # print('display_dict')
        # print(display_dict)

# Broadscasts on port 5678
async def websocket_main(statuses_dict):
    async with websockets.serve(register, "192.168.**.***", 5678):
        await broadcast_statuses(statuses_dict)



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

def on_message(client, userdata, msg):    
    # print("mqtt on_message")
    
    topic = str(msg.topic)
    payload = str(msg.payload)[2:-1]

    if (topic == 'pir-sensor'):
        statuses_dict['pir_state'] = payload
        # print(statuses_dict['pir_state'])
    elif (topic == 'ultrasound'):
        statuses_dict['ult_state'] = int(payload)
    elif (topic == 'doppler-radar'):
        statuses_dict['dop_state'] = int(payload)
    else:
        {print(topic + "is not found.")}
    # print(topic + ' ' + payload)    

def mqtt_loop_function(statuses_dict):
    print('mqtt')
    # print(statuses_dict)

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    # print("Hello")
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def uart_loop_function(statuses_dict):
    isRpi = True
    if (isRpi):
        print('uart is running')
        #print(statuses_dict)
        ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
        while True:
            received_data = ser.read()              #read serial port
            sleep(0.03)
            data_left = ser.inWaiting()             #check for remaining byte
            received_data += ser.read(data_left)
            processed_data = float(str(received_data)[2:-1])
            statuses_dict['uart_state'] = str(processed_data)
        
            # print('uart_state: ')
            # print(statuses_dict['uart_state'])                   #print received data

    else:
        while(True):    
            processed_data = (random.randint(1, 8)+random.randint(1, 8))/2
            statuses_dict['uart_state'] = str(processed_data)
            print(statuses_dict['uart_state'])                   #print received data
            sleep(5.5)

def websocket_loop_function(statuses_dict):
    print('websockets is running')
    # print(statuses_dict)
    asyncio.run(websocket_main(statuses_dict))

if __name__ == '__main__':
    print('main is running')
    
    with Manager() as manager:
        statuses_dict = manager.dict()
        statuses_dict['pir_state'] = 0
        statuses_dict['ult_state'] = 0
        statuses_dict['dop_state'] = 0
        statuses_dict['uart_state'] = 0.0
        # print(statuses_dict)

        p_1 = Process(target=mqtt_loop_function, args=(statuses_dict,))
        p_2 = Process(target=uart_loop_function, args=(statuses_dict,))
        p_3 = Process(target=websocket_loop_function, args=(statuses_dict,))
        
        p_1.start()
        p_2.start()
        p_3.start()
        
        p_1.join()
        p_2.join()
        p_3.join()









