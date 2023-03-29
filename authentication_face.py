import cv2
import os
import time
import numpy as np
import pickle
from PIL import Image
from configtext import ConfigText

config = ConfigText()

class FaceRecogntion(object):
    
    def face_collections(self, name):
        # Set the delay time in seconds
        delay = 10

        # Set the image counter to 0
        img_counter = 0

        #face_cascade = cv2.CascadeClassifier(config.modelxml)
        # Initialize the camera
        camera = cv2.VideoCapture(0)
        camera.set(3,640)
        camera.set(4,480)
        cv2.namedWindow("Scanning Face", cv2.WINDOW_NORMAL)

        # Create a folder to store images
        if not os.path.exists('traning_data/'+ name):
            os.makedirs('traning_data/'+ name)
            
        # Start capturing and saving images
        start_time = time.time()
        prev_frame_time = 0

        # Reduce the quality of the image until the size is below the target size
        quality = 30 # Maximum quality

        # Wait for space key to be pressed
        print("Press the space key to start capturing images within {} seconds...".format(delay))
        while True:
            ret, frame = camera.read()
            cv2.imshow("Scanning Face", frame)
            if cv2.waitKey(1) == ord(' '):
                break
        count = 0
        while True:
            # Read a frame from the camera
            ret, frame = camera.read()

            # Dislaythe FPS
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            cv2.putText(frame, "FPS: {:.2f}".format(fps), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if not ret:
                print("Caturing fail")
                break
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 177, 123], False, False)
            detector = cv2.dnn.readNetFromCaffe(config.protopath, config.modelpath)
            detector.setInput(blob)
            face_detections = detector.forward() 

            for i in range(0, face_detections.shape[2]):
                confidence = face_detections[0, 0, i, 2]
                if confidence > 0.5:
                    face_box = face_detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    (x, y, w, h) = face_box.astype("int")
                    #print(startX, startY, endX, endY)
                    cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
                    crop_image = frame[y:h, x:w]

            if (time.time() - start_time) < delay:
                # Create a countdown timer
                timer = delay - int(time.time() - start_time)

                # Reduce the quality of the image
                # img_encode_param = [cv2.IMWRITE_JPEG_QUALITY, quality]
                # frame_data = cv2.imencode('.jpg', crop_image, img_encode_param)[1].tobytes()
                img = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
                # Save the image to a folder
                img_name = "traning_data/{}/img_{}.jpg".format(name, img_counter)
                cv2.imwrite(img_name, img)
                # with open(img_name, "wb") as f:
                #      f.write(crop_image)

                print("{} saved!".format(img_name))
                img_counter += 1
            else:
                break
            #Display the frame
            cv2.imshow("Scanning Face", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        # Release the camera and close all windows
        camera.release()
        cv2.destroyAllWindows()
        print("Closing collecting data ................")        

    def  training_faces(self):
        data_list = []
        labels_list = []

        for dict_path in os.listdir('traning_data'):
            dict_path = os.path.join('traning_data',dict_path)
            list_filename = []
            for filename in os.listdir(dict_path):
                filename_path = os.path.join(dict_path, filename)
                name = filename_path.split('/')[1]
                img = np.array(cv2.imread(filename_path))
                list_filename.append((img, name))
                labels_list.append(name)
                #print(list_filename)

            data_list.extend(list_filename)
            f = open("labels.pickle", "wb")
            f.write(pickle.dumps(data_list))
        labels_list = np.array(labels_list)
        print(labels_list)

        
fr = FaceRecogntion()
#name = input("Name input :" )
#fr.face_collections(name)
fr.training_faces()
#data = pickle.loads(open('labels.pickle', "rb").read())
#print(data)