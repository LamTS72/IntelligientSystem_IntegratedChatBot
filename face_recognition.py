from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import threading
import time
from sklearn.svm import SVC

#import adafruit_control
from align.align_mtcnn import *
from facenet.face_contrib import *

result_val = {"result_0":None, "result_1":None}
check_val = {"check_0":False,"check_1":False}

class FaceRecognition:
    def __init__(self, data_input='train_data/faces', data_align='align_data', model_pb='models/20180402-114759.pb',
                 classifier_filename='models/trained/trained_model.pkl', batch_size=1000, image_size=160, seed=123,
                 model_checkpoint='models'):
        self.data_input = data_input
        self.data_align = data_align
        self.model_pb = model_pb
        self.classifier_filename = classifier_filename
        self.batch_size = batch_size
        self.image_size = image_size
        self.seed = seed
        self.model_checkpoint = model_checkpoint
        self.cnt = 0

    def face_collections(self, name):
        print("Opening camera for collecting data ................")
        # Set the image counter to 0
        img_counter = 0
        camera = cv2.VideoCapture(0)
        # Create a folder to store images
        if not os.path.exists('train_data/faces/' + name):
            os.makedirs('train_data/faces/' + name)

        count = 0
        prev_frame_time = 0
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

            if cv2.waitKey(1) % 256 == 32:
                img = cv2.resize(frame, (224, 224))
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Save the image to a folder
                img_name = "train_data/faces/{}/img_{}.jpg".format(name, img_counter)
                cv2.imwrite(img_name, img)

                print("{} saved!".format(img_name))
                img_counter += 1
            if img_counter == 15:
                break
            # Display the frame
            cv2.imshow("Collect Face", frame)

            if cv2.waitKey(1) == ord('q'):
                break
        # except:
        # print("No frames")
        # Release the camera and close all windows
        camera.release()
        cv2.destroyAllWindows()
        print("Closing collecting data ................")

    def train_data(self):
        align_mtcnn(self.data_input, self.data_align)
        with tf.Graph().as_default():
            with tf.Session() as sess:
                np.random.seed(seed=self.seed)
                dataset = get_dataset(self.data_align)

                paths, labels = get_image_paths_and_labels(dataset)

                print('Number of classes: %d' % len(dataset))
                print('Number of images: %d' % len(paths))
                # Load the model
                print('Loading feature extraction model')
                load_model(self.model_pb)
                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                embedding_size = embeddings.get_shape()[1]

                # Run forward pass to calculate embeddings
                print('Calculating features for images')
                nrof_images = len(paths)
                nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / self.batch_size))
                emb_array = np.zeros((nrof_images, embedding_size))
                for i in range(nrof_batches_per_epoch):
                    start_index = i * self.batch_size
                    end_index = min((i + 1) * self.batch_size, nrof_images)
                    paths_batch = paths[start_index:end_index]
                    images = load_data(paths_batch, False, False, self.image_size)
                    feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                    emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)

                classifier_filename_exp = os.path.expanduser(self.classifier_filename)

                # Train classifier
                print('Training classifier')
                model = SVC(kernel='linear', probability=True)
                model.fit(emb_array, labels)

                # Create a list of class names
                class_names = [cls.name.replace('_', ' ') for cls in dataset]

                # Saving classifier model
                with open(classifier_filename_exp, 'wb') as outfile:
                    pickle.dump((model, class_names), outfile)
                print('Saved classifier model to file "%s"' % classifier_filename_exp)

    def run_recognition(self, cam):
        global result_val, check_val#, name_recognition_0, name_recognition_1, num_face_0, num_face_1
        frame_interval = 3
        fps_display_interval = 5
        frame_rate = 0
        frame_count = 0
        if cam is not None:
            video_capture = cv2.VideoCapture(cam)
        else:
            video_capture = cv2.VideoCapture(0)
            cam = 0# Use internal camera

        # Create a window to show the camera feed

        ret, frame = video_capture.read()
        width = frame.shape[1]
        height = frame.shape[0]
        window_name = "Video Cam: " + str(cam)
        face_recognition = Recognition(self.model_checkpoint, self.classifier_filename)
        start_time = time.time()
        new_frame_time = time.time()
        frame_cnt = 0
        while True:
            list_name = {}
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            if (frame_count % frame_interval) == 0:
                faces = face_recognition.identify(frame)

                # Check our current fps
                end_time = time.time()
                if (end_time - start_time) > fps_display_interval:
                    frame_rate = int(frame_count / (end_time - start_time))
                    start_time = time.time()
                    frame_count = 0

            # helpier.add_overlays(frame, faces, frame_rate, colors)
            if faces is not None:
                for idx, face in enumerate(faces):
                    face_bb = face.bounding_box.astype(int)
                    cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),  (0, 255, 0), 1)
                    temp_name = {}
                    if face.name and face.prob:
                        if face.prob > 0.7:
                            class_name = face.name
                            self.cnt = self.cnt + 1
                            temp_name = {"name"+str(idx + 1): class_name.upper()}
                        else:
                            class_name = 'Unknown'
                            self.cnt = 0
                            temp_name = {"name" + str(idx + 1): class_name.upper()}
                            # class_name = face.name
                        cv2.putText(frame, class_name, (face_bb[0], face_bb[3] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (0, 255, 0), thickness=2, lineType=2)
                        cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), thickness=1, lineType=2)

                        print(temp_name)
                        list_name.update(temp_name)

                # if cam == 0:
                #     adafruit_control.name_recognition = str(list_name)
                #     adafruit_control.num_face = len(faces)
                #     print(adafruit_control.AdafruitControl.)
                # else:
                #     adafruit_control.name_recognition1 = str(list_name)
                #     adafruit_control.num_face1 = len(faces)

            frame_count += 1
            frame_cnt += 1
            elapsed_time = time.time() - new_frame_time
            fps = frame_cnt / elapsed_time
            cv2.putText(frame, str(fps) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0),
            thickness=2, lineType=2)
            cv2.imshow(window_name, frame)

            if self.cnt == 10:
                if cam == 0:
                    print("OK")
                    video_capture.release()
                    #name_recognition_0 = str(list_name)
                    num_face_0 = len(faces)
                    result_val["result_0"] = "Valid", class_name.upper(),num_face_0
                    check_val["check_0"] = True
                    return result_val["result_0"]
                else:
                    print("OK")
                    video_capture.release()
                    #name_recognition_1 = str(list_name)
                    num_face_1 = len(faces)
                    result_val["result_1"] = "Valid", class_name.upper(), num_face_1
                    check_val["check_1"] = True
                    return result_val["result_1"]
                

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if cam == 0:
                    # adafruit_control.name_recognition = None
                    # adafruit_control.num_face = None
                    #name_recognition = None
                    num_face_0 = None
                else:
                    # adafruit_control.name_recognition1 = None
                    # adafruit_control.num_face1 = None
                    #name_recognition1 = None
                    num_face_1 = None
                break

        video_capture.release()




    def run_multicam_recognition(self):
        # # Camera IDs to capture from
        camera_ids = [0, 1]

        # Create threads for each camera
        threads = []
        for camera_id in camera_ids:
            t = threading.Thread(target=self.run_recognition, args=(camera_id,))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()

        cv2.destroyAllWindows()




# if __name__ == '__main__':
#
#     train('align_data', 'models/20180402-114759.pb', 'models/your_model.pkl')
#fr = FaceRecognition()
# fr.face_collections()
# fr.train_data()
#fr.run_multicam_recognition()
