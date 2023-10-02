import time
from Adafruit_IO import MQTTClient
import sys

class AdafruitControl:
    def __init__(self, username='sonlam7220', key='aio_KWKE08Sfn6cBT0UjORNFRlxfLXES'):
        self.AIO_USERNAME = username
        self.AIO_KEY = key
        self.AIO_FEED_ID = ["sensor1", "sensor2", "notification0", "notification1"]
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.name_recognition = None
        self.name_recognition1 = None
        self.num_face = None
        self.num_face1 = None

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

    
    def communicate_adafruit(self):
        self.client.loop_background()
        counter = 20
        prev_name_recognition = ""
        prev_name_recognition1 = ""
        while True:
            counter -= 1
            if counter <= 0:
                if self.name_recognition != prev_name_recognition:
                    prev_name_recognition = self.name_recognition
                    if self.name_recognition != "[]" and self.name_recognition is not None:
                        self.client.publish("notification0", self.name_recognition)
                        self.client.publish("sensor1", self.num_face)
                else:
                    prev_name_recognition = ""

                if self.name_recognition1 != prev_name_recognition1:
                    prev_name_recognition1 = self.name_recognition1
                    if self.name_recognition1 != "[]" and self.name_recognition1 is not None:
                        self.client.publish("notification1", self.name_recognition1)
                        self.client.publish("sensor2", self.num_face1)
                else:
                    prev_name_recognition1 = ""
            time.sleep(0.5)


