from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from home_page import *
from Adafruit_IO import MQTTClient
from common_share import *

class Startup:
    def __init__(self, root):
        self.root = root
        self.root.geometry("840x550+280+100")
        self.root.title("Smart System For Face Recognition And ChatGPT")
        self.root.resizable(False, False)
        self.root.focus_force()
        bg1 = Image.open("View//bg1.png")
        bg1 = bg1.resize((840, 550))
        self.photo = ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root, image=self.photo)
        bg_img.place(x=0, y=0, width=840, height=550)
        start = Button(bg_img, command=self.run_Home, text="Start", font=("times new roman", 15, "bold"),
                     bd=0, relief=RIDGE, fg="White", bg="#38a728", activeforeground="white", activebackground="#007ACC")
        start.place(x=262, y=500, width=316, height=20)

        exit = Button(bg_img, command=exit_program, text="Exit", font=("times new roman", 15, "bold"),
                       bd=0, relief=RIDGE, fg="White", bg="#38a728", activeforeground="white",
                       activebackground="#007ACC")
        exit.place(x=720, y=500, width=100, height=20)
        self.adafruit_run = AdafruitControl()
        self.run_Ada()

    def run_Home(self):
        self.root.withdraw()
        self.home=Toplevel(self.root)
        self.app=HomeApp(self.home)

    # def exit_program(self):
    #     #sys.exit()
    #     self.adafruit_run.disconnected()

    def run_Ada(self):
        #Using daemon thread that have low priority and run in background without affect other threads
        t = threading.Thread(target=self.adafruit_run.communicate_adafruit, name='t')
        t.daemon = True
        t.start()

if __name__ == "__main__":
    root = Tk()
    obj = Startup(root)
    root.mainloop()