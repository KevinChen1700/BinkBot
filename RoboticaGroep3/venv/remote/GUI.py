#!/usr/bin/env python
from Tkinter import *
import RPi.GPIO as GPIO
import socket
from Joystick import Joystick
from BatteryValue import BatteryValue
import spidev
import time
import os


class Window(Frame):

    def __init__(self, master=None):
        BatteryValue.__instance = self
        self.HOST = "141.252.217.182"
        self.PORT = 5002
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

        self.lastPressed = 'man'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.connect(("8.8.8.8",80))
        self.HOST = self.s.getsockname()[0]
        self.PORT = 5002
        print self.HOST
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print 'Connected by', self.addr
        GPIO.setmode(GPIO.BCM)
        self.joystickBus = Joystick.getInstance()
        self.battery = BatteryValue.getInstance()
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        sdanceButton = Button(self, text="Single Dance", relief=RIDGE, bg="black", fg="white", command=self.client_sdance)
        sdanceButton.place(x=10, y=20)

        ldanceButton = Button(self, text="Line Dance", relief=RIDGE, bg="black", fg="white", command=self.client_ldance)
        ldanceButton.place(x=10, y=70)

        trapButton = Button(self, text="Survival Run", relief=RIDGE, bg="black", fg="white", command=self.client_trap)
        trapButton.place(x=140, y=20)

        eggButton = Button(self, text="Eggtelligence", relief=RIDGE, bg="black", fg="white", command=self.client_egg)
        eggButton.place(x=140, y=70)

        blueButton = Button(self, text="Blue Bar", relief=RIDGE, bg="black", fg="white", command=self.client_blue)
        blueButton.place(x=270, y=20)

        manualButton = Button(self, text="Manual mode", relief=RIDGE, bg="black", fg="white", command=self.manual_mode)
        manualButton.place(x=270, y=70)

        # label to show outputs of the pi
        global lbl
        lbl = Label(self, text="output scherm ", width=50, height=7, wraplength=300, bg="white")
        lbl.place(x=10, y=120)

    # event handler voor als de buttons gedrukt zijn
    def client_sdance(self):
        lbl.config(text="doing single dance..")
        self.lastPressed = "singleDance"

    def client_ldance(self):
        lbl.config(text="doing line dance..")
        self.lastPressed = "lineDance"

    def client_trap(self):
        lbl.config(text="doing survival run..")
        self.lastPressed = "survivalRun"

    def client_egg(self):
        lbl.config(text="doing eggtelligence run..")
        self.lastPressed = "eggTelligence"

    def client_blue(self):
        lbl.config(text="doing blue bar..")
        self.lastPressed = "blue"

    def manual_mode(self):
        #lbl.config(text="cancelling current mode..")
        self.lastPressed = "man"

    def sendstate(self):
        datastring = str(self.joystickBus.readChannel(0)) + "-" + str(self.joystickBus.readChannel(1)) + "-" + str(self.joystickBus.readChannel(2)) + "-" + str(self.joystickBus.readChannel(3)) + "-" + self.lastPressed + "|"
        self.conn.send(datastring)
        print(datastring)

    def getSignal(self):
        temp = self.s.recv(4096)
        return temp



root = Tk()
root.geometry("390x250")
app = Window(root)
while True:
    lbl.config(text=Window.getSignal())
    root.update_idletasks()
    root.update()
    Window.sendstate(app)
    time.sleep(0.03)
