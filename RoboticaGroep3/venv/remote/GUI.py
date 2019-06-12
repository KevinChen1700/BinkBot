# !/usr/bin/env python
from Tkinter import *
import RPi.GPIO as GPIO
import socket
from Joystick import Joystick
import spidev
import time
import os


class Window(Frame):

    def __init__(self, master=None):
        self.lastPressed = 'man'  # string to remember which button has been pressed
        # socket connection to send data from remote
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.connect(("8.8.8.8", 80))
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
        # creates instance of the joystick class to control the physical joysticks
        self.joystickBus = Joystick.getInstance()
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # function to create the gui of the app
    def init_window(self):
        time.sleep(0.1)
        # socket connection to get data from the pi of the robot
        self.HOST = "141.252.217.182"
        self.PORT = 5002
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2.connect((self.HOST, self.PORT))

        # change the title of the app
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # create and place the buttons in the gui
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

        # label to show which action is being performed
        global lbl
        lbl = Label(self, text="output scherm ", width=50, height=7, wraplength=300, bg="white")
        lbl.place(x=10, y=120)

        # label to show the battery voltage of the robot
        global lbl2
        lbl2 = Label(self, text="Accu", width=5, height=1, bg="white")
        lbl2.place(x=10, y=230)

    # functions to change lastPressed with the corresponding action after a button has been pressed
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
        lbl.config(text="cancelling current mode..")
        self.lastPressed = "man"

    # function to send the joystick values and string in lastPressed to the pi of the robot
    def sendstate(self):
        datastring = str(self.joystickBus.readChannel(0)) + "-" + str(self.joystickBus.readChannel(1)) + "-" + str(
            self.joystickBus.readChannel(2)) + "-" + str(self.joystickBus.readChannel(3)) + "-" + self.lastPressed + "|"
        self.conn.send(datastring)
        print(datastring)

    # function to get the battery voltage value of the pi inside the robot
    def getSignal(self):
        temp = self.s2.recv(4096)
        return temp


root = Tk()
root.geometry("390x250")
app = Window(root)
# main loop
while True:
    battery = Window.getSignal(app)  # stores the value of the battery voltage

    root.update_idletasks()
    root.update()
    Window.sendstate(app)
    try:
        if (int(battery) == 1023):   # changes the background color of the battery label to green when value is 1023
            lbl2.config(bg="green")
        # changes the background color of the battery label to red when value is lower than 981
        elif (int(battery) < 981):
            lbl2.config(bg="red")
        else:
            lbl2.config(bg="blue")  # changes the background color of the battery label to blue when no value is read
    except Exception:
        pass



