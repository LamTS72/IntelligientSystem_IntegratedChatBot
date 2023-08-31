from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from home import *



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

        exit = Button(bg_img, command=self.exit_program, text="Exit", font=("times new roman", 15, "bold"),
                       bd=0, relief=RIDGE, fg="White", bg="#38a728", activeforeground="white",
                       activebackground="#007ACC")
        exit.place(x=720, y=500, width=100, height=20)

    def run_Home(self):
        root.withdraw()
        self.home=Toplevel(self.root)
        self.app=HomeApp(self.home)

    def exit_program(self):
        sys.exit()

if __name__ == "__main__":
    run_ada = AdafruitControl()
    t = threading.Thread(target=run_ada.run_adafruit, name='t')
    t.daemon = True
    t.start()
    root = Tk()
    obj = Startup(root)
    root.mainloop()