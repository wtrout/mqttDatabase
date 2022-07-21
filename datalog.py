import sqlite3
import paho.mqtt.client as mqtt
import time

db_file = "data.db"

def writeLine(table, data):
    tNow = int(time.time())
    print(f"Writing {data} to {table} table at {tNow}")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table} VALUES({tNow},{data})")
    conn.commit()
    conn.close()

def on_temp0_message(client, userdata, message): #OUTSIDE
    writeLine("outsideTemp", float(message.payload.decode('ASCII').strip('/r')))

def on_temp1_message(client, userdata, message): #GARAGE
    writeLine("garageTemp", float(message.payload.decode('ASCII').strip('/r')))

def on_temp2_message(client, userdata, message): #KITCHEN
    writeLine("kitchenTemp", float(message.payload.decode('ASCII').strip('/r')))

def on_connect(client, userdata, flags, rc):
    client.subscribe( [('garage/temp0',0), ('garage/temp1',0),('garage/temp2',0)] )
    client.message_callback_add('garage/temp0', on_temp0_message)
    client.message_callback_add('garage/temp1', on_temp1_message)
    client.message_callback_add('garage/temp2', on_temp2_message)



client = mqtt.Client()
client.username_pw_set(<REDACTED>)
client.on_connect = on_connect
client.connect(<REDACTED>)
client.loop_forever()
