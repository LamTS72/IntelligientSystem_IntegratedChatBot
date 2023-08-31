from tkinter import*
from tkinter import ttk
from PIL import ImageTk
from PIL import Image

from face_recognition import *
from chatbot_ui import *

class HomeApp(tk.Toplevel):
    def __init__(self, root, classifier_filename='models/trained/trained_model.pkl', model_checkpoint='models'):
        self.classifier_filename = classifier_filename
        self.model_checkpoint = model_checkpoint
        self.root = root
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.title("Smart System For Face Recognition And ChatGPT")
        self.root.geometry("840x550+280+100")
        bg1 = Image.open(r"View//home.jpg")
        bg1 = bg1.resize((840, 550))
        self.photo = ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root, image=self.photo)
        bg_img.place(x=0, y=0, width=840, height=550)

        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        chatbot_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Chatbot", menu=chatbot_menu)
        chatbot_menu.add_command(label="Open ChatGPT", command=self.show_chatbot_app)

        camera_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Camera", command=lambda: threading.Thread(target=self.start_cam).start())

        camera_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Register", command=lambda: threading.Thread(target=self.start_register).start())

        quit_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Exit", command=lambda: sys.exit(1))

#//////////////////////////////////////////////////////////////////////
        # # Create canvas for video frames
        # self.canvas = tk.Canvas(self.root,  width=640, height=480)
        # self.canvas.pack(side="top", padx=5, pady=5)

        # if self.cam is not None:
        #     self.video_capture = cv2.VideoCapture(self.cam)
        # else:
        #     self.video_capture = cv2.VideoCapture(0)

        #self.fr = FaceRecognition()
        #self.face_recognition = Recognition(self.model_checkpoint, self.classifier_filename)
        #thread1 = threading.Thread(target=self.fr.run_multicam_recognition)
        #thread1.start()
        #self.update_video_feed(self.cam)
    def start_cam(self):
        fr = FaceRecognition()
        fr.run_multicam_recognition()

    def start_register(self):
        fr = FaceRecognition()
        fr.face_collections()
        fr.train_data()


    def update_video_feed(self, cam):
        # Get video frame from face recognition object
        ret, frame = self.fr.dev_forGUI(self.video_capture, self.face_recognition)
        # Update video feed in canvas
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.imgtk = imgtk
            self.canvas.create_image(0, 0, anchor="nw", image=imgtk)
        # Schedule next update
        self.root.after(1, self.update_video_feed, cam)


    def show_chatbot_app(self):
        # Create the chatbot app window
        chatbot_window = tk.Toplevel(self.root)
        chatbot_app = ChatbotApp(chatbot_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = HomeApp(root)
    root.mainloop()
