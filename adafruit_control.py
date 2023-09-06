import time

from Adafruit_IO import MQTTClient
import sys

name_recognition = None
name_recognition1 = None
num_face = None
num_face1 = None

class AdafruitControl:
    def __init__(self, username='', key=''):
        self.AIO_USERNAME = username
        self.AIO_KEY = key
        self.AIO_FEED_ID = ["sensor1", "sensor2", "notification0", "notification1"]
        #self.run_adafruit()

    def connected(self, client):
        print("Connected successful ...")
        #subcribe IO-feeds in adafruit from python gateway
        for i in self.AIO_FEED_ID:
            client.subscribe(i)

    def subscribe(self, client, userdata, mid, granted_qos):
        #notification of finish subcriber feeds to client
        print("Subscribe successful ...")

    def disconnected(client):
        print("Disconnected...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        #notification of receiving data from feeds to client
        print("Receiving data: " + payload + " from feed id: " + feed_id)

    def run_adafruit(self):
        client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        client.on_connect = self.connected
        client.on_disconnect = self.disconnected
        client.on_message = self.message
        client.on_subscribe = self.subscribe
        client.connect()
        client.loop_background()
        counter = 20
        prev_name_recognition = ""
        prev_name_recognition1 = ""
        while True:
            counter -= 1
            if counter <= 0:
                if name_recognition != prev_name_recognition:
                    prev_name_recognition = name_recognition
                    if name_recognition != "[]" and name_recognition is not None:
                        client.publish("notification0", name_recognition)
                        client.publish("sensor1", num_face)

                if name_recognition1 != prev_name_recognition1:
                    prev_name_recognition1 = name_recognition1
                    if name_recognition1 != "[]" and name_recognition1 is not None:
                        client.publish("notification1", name_recognition1)
                        client.publish("sensor2", num_face1)
            time.sleep(0.5)

