import time
from Adafruit_IO import MQTTClient
import sys
from dotenv import dotenv_values
import face_recognition
config = dotenv_values(".env")

connected_done = False
authenticate_val = {"door0":"Invalid","door1":"Invalid"}
payload_val = {"door0":"","door1":""}
count_time ={"door0":"","door1":""}
counter = 0
timer_flag = False

class AdafruitControl:
    def __init__(self):
        self.AIO_USERNAME = config.get("ADAFRUIT-NAME")
        self.AIO_KEY = config.get("ADAFRUIT-KEY")
        self.AIO_FEED_ID = ["cam0", "cam1", "notification0", "notification1","door0","door1"]
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.recognition_list = {"name_recognition_0":None, "name_recognition_1":None}
        self.num_face_list = {"num_face_0":None, "num_face_1":None}


    def connected(self, client):
        global connected_done
        #subcribe IO-feeds in adafruit from python gateway
        for i in self.AIO_FEED_ID:
            client.subscribe(i)
        print("Connected successful ...")
        connected_done = True
        return connected_done

    def subscribe(self, client, userdata, mid, granted_qos):
        #notification of finish subcriber feeds to client
        #print("Subscribe successful ...")
        pass

    def disconnected(client):
        print("Disconnected...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        global payload_val
        #notification of receiving data from feeds to client
        print("Receiving data: " + payload + " from feed id: " + feed_id)
        if feed_id == "door0":
            payload_val["door0"] = payload

        elif feed_id == "door1":
            payload_val["door1"] = payload

    def control_door(self, result, door, cam, check, name_recognition, num_face, notification):
        global result_val, check_val, authenticate_val, counter, timer_flag
        print(face_recognition.result_val[result])
        authenticate_val[door], self.recognition_list[name_recognition],self.num_face_list[num_face] = face_recognition.result_val[result]
        if authenticate_val[door] == "Valid":
            self.client.publish(notification,  self.recognition_list["name_recognition_0"])
            self.client.publish(cam, self.num_face_list["num_face_0"])
            self.client.publish(door, config.get("DEVICE-ON"))
            count_time[door] = True
            counter = int(config.get("TIMER-DOOR"))
            timer_flag = True
            face_recognition.result_val[result] = None
            face_recognition.check_val[check] = False

    def communicate_adafruit(self):
        self.client.loop_background()
        global result_val, check_val, authenticate_val,counter, timer_flag

        while True:
            if timer_flag == True:
                print(counter)
                counter -= 1
                if counter <= 0:
                    timer_flag = False
                    if count_time["door0"] == True and payload_val["door0"] == config.get("DEVICE-ON"):
                        self.client.publish("door0", config.get("DEVICE-OFF"))
                        count_time["door0"] = False

                    if count_time["door1"] == True and payload_val["door1"] == config.get("DEVICE-ON"):
                        self.client.publish("door1", config.get("DEVICE-OFF"))
                        count_time["door1"] = False
                        

            
            if face_recognition.check_val["check_0"] == True:
                self.control_door("result_0","door0","cam0","check_0","name_recognition_0","num_face_0","notification0")

            if face_recognition.check_val["check_1"] == True:
                self.control_door("result_1","door1","cam1","check_1","name_recognition_1","num_face_0","notification1")

            time.sleep(0.5)  


