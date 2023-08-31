from tkinter import*
from tkinter import ttk, simpledialog
from PIL import ImageTk
from PIL import Image

from face_recognition import *
from chatbot_ui import *
from adafruit_control import *

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


        #title section
        title = Label(bg_img, text="Smart System For Face Recognition And ChatGPT",
                      font=("verdana", 12, "bold"), bg="white", fg="navyblue")
        title.place(x=0, y=0, width=840, height=45)

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

        # register button
        reg_box = Image.open(r"View\cam.jpg")
        reg_box = reg_box.resize((90, 90))
        self.register_box = ImageTk.PhotoImage(reg_box, Image.LANCZOS)
        reg_btn = Button(bg_img, command=self.start_register, image=self.register_box, cursor="hand2")
        reg_btn.place(x=120, y=200, width=90, height=90)
        reg_btn1 = Button(bg_img, command=self.start_register, text="Register", cursor="hand2",
                          font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
        reg_btn1.place(x=120, y=290, width=90, height=40)


        # recognition button
        recog_box = Image.open(r"View\recognition.jpg")
        recog_box = recog_box.resize((90, 90))
        self.recognition_box = ImageTk.PhotoImage(recog_box, Image.LANCZOS)
        recog_btn = Button(bg_img, command=self.start_cam, image=self.recognition_box, cursor="hand2")
        recog_btn.place(x=300, y=200, width=90, height=90)
        recog_btn1 = Button(bg_img, command=self.start_cam, text="Recognition", cursor="hand2",
                          font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
        recog_btn1.place(x=300, y=290, width=90, height=40)

        # chatgpt button
        chat_box = Image.open(r"View\chat.jpg")
        chat_box = chat_box.resize((90, 90))
        self.chatgpt_box = ImageTk.PhotoImage(chat_box, Image.LANCZOS)
        chat_btn = Button(bg_img, command=self.show_chatbot_app, image=self.chatgpt_box, cursor="hand2")
        chat_btn.place(x=120, y=380, width=90, height=90)
        chat_btn1 = Button(bg_img, command=self.show_chatbot_app, text="ChatGPT", cursor="hand2",
                          font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
        chat_btn1.place(x=120, y=470, width=90, height=40)

        # exit button
        exit_box = Image.open(r"View\exi.jpg")
        exit_box = exit_box.resize((90, 90))
        self.quit_box = ImageTk.PhotoImage(exit_box, Image.LANCZOS)
        quit_btn = Button(bg_img, command=self.exit_program, image=self.quit_box, cursor="hand2")
        quit_btn.place(x=300, y=380, width=90, height=90)
        quit_btn1 = Button(bg_img, command=self.exit_program, text="Exit", cursor="hand2",
                          font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
        quit_btn1.place(x=300, y=470, width=90, height=40)

    def exit_program(self):
        sys.exit()

    def start_cam(self):
        fr = FaceRecognition()
        fr.run_multicam_recognition()


    def start_register(self):
        name = simpledialog.askstring("Enter Name", "Please enter name:")
        fr = FaceRecognition()
        fr.face_collections(name)
        fr.train_data()
        messagebox.showinfo("Message Box", "Collection and Completed Training")


    def show_chatbot_app(self):
        chatbot_window = tk.Toplevel(self.root)
        chatbot_app = ChatbotApp(chatbot_window)



