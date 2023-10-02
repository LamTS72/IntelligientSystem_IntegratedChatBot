from tkinter import*
from tkinter import ttk, simpledialog, messagebox
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import time
import threading
from face_recognition import *
from adafruit_control import *
import openai
from PIL import Image, ImageTk
from speech2text import *
from common_share import *

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
        chatbot_menu.add_command(label="Open ChatGPT", command=self.start_chatbot)

        camera_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Camera", command=lambda: threading.Thread(target=self.start_cam).start())

        register_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Register", command=lambda: threading.Thread(target=self.start_register).start())

        quit_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Exit", command=lambda: exit_program())

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
        chat_btn = Button(bg_img, command=self.start_chatbot, image=self.chatgpt_box, cursor="hand2")
        chat_btn.place(x=120, y=380, width=90, height=90)
        chat_btn1 = Button(bg_img, command=self.start_chatbot, text="ChatGPT", cursor="hand2",
                          font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
        chat_btn1.place(x=120, y=470, width=90, height=40)


        # exit button
        exit_box = Image.open(r"View\exi.jpg")
        exit_box = exit_box.resize((90, 90))
        self.quit_box = ImageTk.PhotoImage(exit_box, Image.LANCZOS)
        quit_btn = Button(bg_img, command=exit_program, image=self.quit_box, cursor="hand2")
        quit_btn.place(x=300, y=380, width=90, height=90)
        quit_btn1 = Button(bg_img, command=exit_program, text="Exit", cursor="hand2",
                          font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
        quit_btn1.place(x=300, y=470, width=90, height=40)
       
    def start_cam(self):
        fr = FaceRecognition()
        fr.run_multicam_recognition()


    def start_register(self):
        name = simpledialog.askstring("Enter Name", "Please enter name:")
        fr = FaceRecognition()
        fr.face_collections(name)
        fr.train_data()
        messagebox.showinfo("Message Box", "Collection and Completed Training")


    def start_chatbot(self):
        self.root.withdraw()
        self.chatbot_window = Toplevel(self.root)
        self.chatbot_app = ChatbotApp(self.chatbot_window)


#openai.api_key = "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"
openai.api_key = "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"

class ChatbotApp(tk.Toplevel):
    def __init__(self, root):
        self.root = root
        self.root.title("OpenAI ChatGPT")
        self.talk = False
        self.vietnamese = True
        self.message_history = []
        self.create_widgets()

    def create_widgets(self):
        # Create scrollable input text
        input_frame = ttk.Frame(self.root)
        input_frame.pack(side="bottom", fill="x")

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        back_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Back", command=lambda: self.back_homepage())

        quit_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Exit", command=lambda: exit_program())

        input_scroll = ttk.Scrollbar(input_frame, orient="vertical")
        self.input_text = tk.Text(input_frame, height=10, yscrollcommand=input_scroll.set)
        input_scroll.config(command=self.input_text.yview)

        input_scroll.pack(side="right", fill="y")
        self.input_text.pack(side="left", fill="both", expand=True)

        # Create scrollable output text
        output_frame = ttk.Frame(self.root)
        output_frame.pack(side="top", fill="both", expand=True)

        output_scroll = ttk.Scrollbar(output_frame, orient="vertical")
        self.output_text = tk.Text(output_frame, height=20, yscrollcommand=output_scroll.set)
        output_scroll.config(command=self.output_text.yview)

        output_scroll.pack(side="right", fill="y")
        self.output_text.pack(side="left", fill="both", expand=True)

        self.input_text.bind("<Return>", self.handle_input)

        # Create the label
        self.label = tk.Label(self.root)
        self.label.pack(side="top")
        self.label.config(text="")

        # Create micro button
        micro_box = Image.open(r"View//micro.png")
        micro_box = micro_box.resize((30, 30))
        self.micro_img = ImageTk.PhotoImage(micro_box, Image.LANCZOS)
        self.micro_button1 = ttk.Button(input_frame, command=lambda: threading.Thread(target=self.handle_inputspeech).start(),
                                   image=self.micro_img, cursor="hand2")

        self.micro_button1.pack(side="right", padx=5)
        # Create send button
        send_box = Image.open(r"View//tra1.jpg")
        send_box = send_box.resize((30, 30))
        self.send_img = ImageTk.PhotoImage(send_box, Image.LANCZOS)
        self.submit_button = ttk.Button(input_frame, text="SEND", command=self.handle_input,
                                   image=self.send_img, cursor="hand2")
        self.submit_button.pack(side="right", padx=5)

        # Create language button
        flag_box = Image.open(r"View//vn.jpg")
        flag_box = flag_box.resize((20, 20))
        self.flag_img = ImageTk.PhotoImage(flag_box, Image.LANCZOS)
        self.flag_button = ttk.Button(input_frame, command=self.handle_languages,
                                   image=self.flag_img, cursor="hand2")
        self.flag_button.pack(side="left", padx=5)


    def back_homepage(self):
        self.root.withdraw()
        self.home=Toplevel(self.root)
        self.app=HomeApp(self.home)


    def generate_response(self, user_input, role="user"):

        array_exit = ["", "Bye ChatGPT", " Bye ChatGPT", "bye", "bye chat", " bye", " see you"]
        if user_input in array_exit:
            return None

        self.message_history.append({"role": role, "content": f"{user_input}"})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_history
        )
        response = completion.choices[0].message.content.strip()
        print(response)
        self.message_history.append({"role": "assistant", "content": f"{response}"})
        return response
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=user_input,
        #     max_tokens=4000,
        #     n=1,
        #     stop=None,
        #     temperature=0.5,
        # )
        # return response.choices[0].text.strip()


    def handle_input(self, event=None):
        user_text = self.input_text.get("1.0", "end-1c")
        self.input_text.delete("1.0", tk.END)
        def handle_wthread():
            array_exit = ["", "Bye ChatGPT", " Bye ChatGPT", "bye", "bye chat", " bye", " see you"]
            response_text = self.generate_response(user_text, role="user")
            if response_text is not None:
                self.output_text.insert(tk.END, "You: " + user_text + "\n")
                self.output_text.insert(tk.END, "Chatbot: " + "\n")
                self.output_text.insert(tk.END, response_text + "\n")
                if self.talk is True:
                    text2speech(response_text, self.vietnamese)
                    self.talk = False
            if user_text.strip().lower() in array_exit:
                self.root.destroy()

        # Create a new thread to run handle_input_thread
        input_thread = threading.Thread(target=handle_wthread)
        input_thread.start()

    def handle_inputspeech(self, event=None):
        self.label.config(text="Listening......")
        self.talk = True
        text = get_audio(self.vietnamese)
        self.label.config(text="")
        self.input_text.insert(tk.END, text)
        time.sleep(2)
        self.handle_input()

    def handle_languages(self):
        if self.vietnamese == True:
            self.vietnamese = False
            flag_box = Image.open(r"View//uk.jpg")
            flag_box = flag_box.resize((20, 20))
            self.flag_img = ImageTk.PhotoImage(flag_box, Image.LANCZOS)
            self.flag_button.config(image=self.flag_img)
        else:
            self.vietnamese = True
            flag_box = Image.open(r"View//vn.jpg")
            flag_box = flag_box.resize((20, 20))
            self.flag_img = ImageTk.PhotoImage(flag_box, Image.LANCZOS)
            self.flag_button.config(image=self.flag_img)


