from Tkinter import *
import RPi.GPIO as GPIO
import socket
from Joystick import Joystick
import spidev
import time
import os


class Window(Frame):

    def __init__(self, master=None):
        self.lastPressed = ' '
        self.HOST = '141.252.230.54'
        self.PORT = 5002
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print 'Connected by', self.addr
        GPIO.setmsode(GPIO.BCM)
        self.Joystick1 = Joystick(1, 2)
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        sdansButton = Button(self, text="Single Dans", relief=RIDGE, bg="black", fg="white", command=self.client_sdans)
        sdansButton.place(x=10, y=20)

        ldansButton = Button(self, text="Line Dans", relief=RIDGE, bg="black", fg="white", command=self.client_ldans)
        ldansButton.place(x=10, y=70)

        trapButton = Button(self, text="Survival Run", relief=RIDGE, bg="black", fg="white", command=self.client_trap)
        trapButton.place(x=140, y=20)

        eggButton = Button(self, text="Eggtelligence", relief=RIDGE, bg="black", fg="white", command=self.client_egg)
        eggButton.place(x=140, y=70)

        flagButton = Button(self, text="Capture the flag", relief=RIDGE, bg="black", fg="white", command=self.client_flag)
        flagButton.place(x=270, y=20)

        manualButton = Button(self, text="Manual mode", relief=RIDGE, bg="black", fg="white", command=self.manual_mode)
        manualButton.place(x=270, y=70)

        # label to show outputs of the pi
        global lbl
        lbl = Label(self, text="output scherm ", width=50, height=7, wraplength=300, bg="white")
        lbl.place(x=10, y=120)

    # event handler voor als de buttons gedrukt zijn
    def client_sdans(self):
        lbl.config(text="doing single dans..")
        self.lastPressed = "sdans"

    def client_ldans(self):
        lbl.config(text="doing line dans..")
        self.lastPressed = "ldans"

    def client_trap(self):
        lbl.config(text="doing survival run..")
        self.lastPressed = "srun"

    def client_egg(self):
        lbl.config(text="doing eggtelligence run..")
        self.lastPressed = "etelligence"

    def client_flag(self):
        lbl.config(text="doing capture the flag..")
        self.lastPressed = "ctf"

    def manual_mode(self):
        lbl.config(text="cancelling current mode..")
        self.lastPressed = "man"

    def sendstate(self):
        datastring = str(self.Joystick1.getX()) + "-" + str(self.Joystick1.getY()) + "-" + self.lastPressed
        self.conn.send(datastring)



root = Tk()
root.geometry("390x250")
app = Window(root)
while True:
    root.update_idletasks()
    root.update()
    Window.sendstate(app)

