import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_ID = ["bbc-led","bbc-humid", "bbc-rgb", "bbc-door"]
AIO_USERNAME = "thuyenpham"
AIO_KEY = ""

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):   
    if (feed_id == "bbc-led"):
        if (payload == "0"):
            print("Nhan du lieu: TAT LED \n")
            ser.write((str("0")).encode())
        else:
            print("Nhan du lieu: BAT LED \n")
            ser.write((str("1")).encode())
        
    elif (feed_id == "bbc-rgb"):
        if (payload == "#0000ff"): #XANH DUONG
            print("Nhan du lieu: XANH DUONG \n")
            ser.write((str("2")).encode())
        elif (payload == "#ff0000"): #DO
            print("Nhan du lieu: DO")
            ser.write((str("3")).encode())
        elif (payload == "#008000"): #XANH LA
            print("Nhan du lieu: XANH LA")
            ser.write((str("4")).encode())
        elif (payload == "#ffff00"): #VANG
            print("Nhan du lieu: VANG")
            ser.write((str("5")).encode())
        else:
            print("Xin chon mau khac")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    # ports = serial.tools.list_ports.comports()
    # N = len(ports)
    # commPort = "None"
    # for i in range(0, N):
    #     port = ports[i]
    #     strPort = str(port)
    #     if "USB Serial Device" in strPort:
    #         splitPort = strPort.split(" ")
    #         commPort = (splitPort[0])
    # return commPort
    return "COM6"

isMicrobitConnected = False
if getPort()!= "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    print("GetPort Thanh Cong")
    isMicrobitConnected = True
    

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        client.publish("bbc-temp", splitData[2])
    elif splitData[1] == "HUMID":
        client.publish("bbc-humid", splitData[2])

mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    if isMicrobitConnected:
        readSerial(client)
    time.sleep(1)