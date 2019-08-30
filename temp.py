import sys
import socket
import select
import os
import glob
import time as tm
import RPi.GPIO as gp
import RPi.GPIO as rp
import RPi.GPIO as GPIO # always needed with RPi.GPIO
from time import sleep # pull in the sleep function from time module 
pause_time=0.02        # you can change this to slow down/speed up
HOST =' '             # symboli name meaning the locsl host
PORT =7728            #Arbitrary non-privileged port

gp.setmode(gp.BOARD)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18,GPIO.OUT)#set GPIO 25 as output for white led
GPIO.setup(24,GPIO.IN,GPIO.PUD)#set GPIO 25 as Input for temperature sensor

#getting sensors into system
os.system('modprobe w1-gpio')
os.system('madprobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder=glob.glob(base_dir+'*28')[0]
device_file=device_folder+'/w1_slave'
s = socket.socket(socket.AF_INET,socket.SOCK_STREM) #socket opening
print ( "Socket created")
try:
    s.bind((HOST,PORT)) # socket blinding
except socket.error_msg:
    print ("Bind failed.Error code: ' + str(msg[0]) + 'Error message: " + msg[1])
    sys.exit()
    print ("Socket Bind comlete")
    s.listen(1) #socket listening
    print ("Socket now listening")
    
def read_temp_raw():
    f=open(device_file,'r')
    lines=f.readlines()
    f.close()
    return lines

while 1:
    conn, addr = s.accept() #socket accepting
    print ("Connected with " +[0] + " : " + str(addr[1]))
    data = conn.recv(5)
    reply = 'ok...' + data
    read_temp()
    
    conn.close()
    
def read_temp():
    lines=read_temp_raw()
    while lines[0].strip() [-3:]!='YES' :
        time.sleep(0.2)
        lines=read_temp_raw()
    equals_pos=lines[1].find( 't=' )
    if equals_pos!=-1:
        temp_string=lines[1][equals.pos+2:]
        temp_c=float(temp_string)/1000.0
        temp_f=temp_c*9.0/5.0+32.0
        conn.send(temp_c,temp_f)
s.close()
GPLO.cleanup()
def getTempForFile(self,file):
    try:
        f = open(self.tempDir + file + "/w1_slave",'r')
    except IOError as e:
        print ("Error: File " + self.tempDir + "/w1_slave" + " doesn't exist")
        return;
        lines=f.readlines()
        crcLine=lines[0]
        tempLine=lines[1]
        result_list = tempLine.split("=")
        temp = float(result_list[-1])/1000 # temp in Celcius
        temp = temp + self.correctionFactor # correction factor
        #if you want to convert to Celcius, comment this line
        temp = (9.0/5.0)*temp + 32
        if crcLine.find("NO") > -1:
            temp = -999
            if(self.debug):
                print ("Current: " + str(temp) + "" + str(file))
                return float(int(temp*100))/100  