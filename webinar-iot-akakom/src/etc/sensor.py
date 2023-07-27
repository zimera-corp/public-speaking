import paho.mqtt.client as mqtt , os, urllib.parse
import time
import random

# Define event callbacks
def on_connect(mosq, obj, flags, rc):
    print ('on_connect:: Connected with result code '+ str ( rc ) )
    print('rc: ' + str(rc))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_log(mosq, obj, level, string):
    print(string)

client = mqtt.Client()
# Assign event callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Uncomment to enable debug messages
client.on_log = on_log

# user name has to be called before connect - my notes.
client.username_pw_set('uqlbaqem', 'imFuSxZS5hYi')

#Connect to the Broker
client.connect('m20.cloudmqtt.com', 14819, 60)
time.sleep(1)

client.loop_start()

run = True

sensordata = ['on', 'off']
print(random.choice(sensordata))

try:
	while run:
	#Send messages to the Broker
		print('Sending \"' + random.choice(sensordata) + '\" to the actuator')
		client.publish ( "/IoTSensor/Sensor01", random.choice(sensordata))
		time.sleep(1)

except KeyboardInterrupt:
    print ('exiting')
    client.disconnect()
    client.loop_stop()
