import sys
import time
from tkinter import*
from tkinter import ttk, messagebox
import threading
import tkinter as tk
from tkinter import ttk
import openai
from PIL import Image, ImageTk
from speech2text import *

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
        quit_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Exit", command=self.root.destroy)

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


