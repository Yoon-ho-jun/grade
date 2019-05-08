#!/usr/bin/env python
import smbus
import time
import math
import sys
import RPi.GPIO as GPIO
import os
import subprocess


os.system('python bluetooth_echo.py&')

os.system('python distance.py&')

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER=17   #ultra sensor
GPIO_ECHO=27


GPIO.setup(14,GPIO.OUT) #Led
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

PCA9685_MODE1=0x0
PCA9685_PRESCALE=0xFE

LED0_ON_L=0x6
LED0_ON_H=0x7
LED0_OFF_L=0x8
LED0_OFF_H=0x9


def read_byte(adr):
    return bus.read_byte_data(address,adr)
def write_byte_2c(adr,val):
    return bus.write_byte_data(address,adr,val)
def write_word_2c(adr,val):
    bus.write_byte_data(address,adr,val)
    bus.write_byte_data(address,adr+1, (val >> 8))
def set_PWMFreq(freq):
    freq *=0.9
    prescaleval = 25000000.0
    prescaleval /= 4095
    prescaleval /= freq
    prescaleval -= 1;

    prescale = math.floor(prescaleval + 0.5)

    oldmode = read_byte(PCA9685_MODE1)
    newmode = (oldmode&0x7F) | 0x10
    write_byte_2c(PCA9685_MODE1,newmode)
    write_byte_2c(PCA9685_PRESCALE,int(prescale))
    time.sleep(0.005)
    write_byte_2c(PCA9685_MODE1,oldmode | 0xa1)
def set_PWM(channel,on,off):
    on = on & 0xFFFF
    off = off & 0xFFFF
    write_word_2c(LED0_ON_L+4*channel,on)
    write_word_2c(LED0_ON_L+4*channel+2,off)
def set_PWM_Duty(channel,rate):
    on = 0
    off = rate*41
    set_PWM(channel, on, int(off))


def left_s(start, end):
    print("left 9.0");  '4 motor op'  #motor 1 left
    for x in range(start,end):
        set_PWM_Duty(x,9.0)


def left(start, end):
    print("left 8.5");  '4 motor op'  #motor 1 left
    for x in range(start,end):
        set_PWM_Duty(x,8.5)

def lef(start, end):
    print("left 5");  '4 motor op'  #motor 1 left
    for x in range(start,end):
        set_PWM_Duty(x,11)        

def left_l(start, end):
    print("left 8");  '4 motor op'
    for x in range(start,end):
        set_PWM_Duty(x,8.0)

def left_ll(start, end):
    print("left 7.5");  '4 motor op'
    for x in range(start,end):
        set_PWM_Duty(x,7.5)

def mid(start, end):
    print("mid 7");  
    for x in range(start,end):
        set_PWM_Duty(x,7.0)

def right_rr(start, end):
    print("right 6.5");
    for x in range(start,end):
        set_PWM_Duty(x,6.5)

def right_r(start, end):
    print("right 6.0");
    for x in range(start,end):
        set_PWM_Duty(x,6.0)

def right(start, end):
    print("right 5.5");
    for x in range(start,end):
        set_PWM_Duty(x,5.5)

def righ(start, end):
    print("right 4.0");
    for x in range(start,end):
        set_PWM_Duty(x,4.0)

def left_curve(start, end):   
    print("left_curve");
    for x in range(start,end):
        set_PWM_Duty(x,2.5)

def right_curve(start, end):
    print("right_curve");
    for x in range(start,end):
        set_PWM_Duty(x,10.5)

def up_left(start, end):
    print("up_left");
    for x in range(start,end):
        set_PWM_Duty(x,11.0)

def up_right(start, end):
    print("up_right");
    for x in range(start,end):
        set_PWM_Duty(x,3.0)

def sw_val():
    f = open('sw.txt', 'r')
    val = f.read()
    f.close()
    return val

def distance_val():
    f = open('distance.txt', 'r')
    val = f.read()
    f.close()
    return val


def move(dir):

    if(dir==1):             #go straight

        mid(0,9)
        time.sleep(0.8)
        
        righ(1,2)
        time.sleep(0.8)
        righ(5,6)
        time.sleep(0)
        righ(3,4)
        time.sleep(0.8)

        mid(5,6)
        time.sleep(0.8)
        mid(3,4)
        time.sleep(0.8)
        mid(1,2)
        time.sleep(0.8)

        mid(6,7)
        time.sleep(0.4)
        
        
        
    elif(dir==2):           #left_curve turn_right  30 deg
        
        righ(6,7)
        time.sleep(0.1)
        lef(4,5)
        time.sleep(0.1)
        lef(2,3)
        time.sleep(0.1)
        lef(0,1)
        time.sleep(0.1)

        mid(0,1)
        time.sleep(0.1)
        mid(2,3)
        time.sleep(0.1)
        mid(4,5)
        time.sleep(0.1)
        mid(6,7)
        time.sleep(0.1)


    elif(dir==3):           #turn_right  30deg

        mid(0,9)
        time.sleep(0.05)

       
        right(6,7)
        time.sleep(0.05)
        left_curve(0,1)
        time.sleep(0.05)
        mid(1,2)
        time.sleep(0.05)
        left_curve(2,3)
        time.sleep(0.05)
        right(7,8)
        time.sleep(0.05)
        left_curve(4,5)
        time.sleep(0.05)
        mid(5,6)
        time.sleep(0.05)
        left_curve(8,9)
        time.sleep(0.1)
        
        for i in range (0,9):
            mid(i,i+1)
            time.sleep(1)


    elif(dir == 4):     #move right

                
        for i in range (0,9):
            if(i == 0):
                right(6,7)

            else:
                if(i%2==0):
                    left(i,i+1)
                elif(i%2 ==1):
                    right(i,i+1)

        for i in range (0,9):
            if(i == 0):
                left(6,7)

            else:
                if(i%2==0):
                    right(i,i+1)
                elif(i%2 ==1):
                    left(i,i+1)


    elif(dir == 5):     # move left

                
        for i in range (0,9):

            if(i%2==0):
                right(8-i,9-i)
            elif(i%2 ==1):
                right(8-i,9-i)
            right(0,1)

        for i in range (9,0,-1):
            if(i%2==0):
                left(8-i,9-i)
            elif(i%2 ==1):
                left(8-i,9-i)

            left(0,1)

    elif(dir == 6):   #left_turn

                
        for i in range (8,-1,-1):
            if(i == 0):
                left(6,7)

            else:
                if(i%2==0):
                    right(i,i+1)
                elif(i%2 ==1):
                    left(i,i+1)

        for i in range (8,-1,-1):
            if(i == 0):
                right(6,7)

            else:
                if(i%2==0):
                    right(i,i+1)
                elif(i%2 ==1):
                    right(i,i+1)                    


    elif(dir==7):            #up and cam
        mid(0,9)
        time.sleep(0.5)
        
        right(5,6)
        os.system('raspistill -t 1 -o 1.jpg')
        time.sleep(0.5)
        right_rr(6,7)
        os.system('raspistill -t 1 -o 2.jpg')
        time.sleep(0.5)
        right_r(6,7)
        os.system('raspistill -t 1 -o 3.jpg')
        time.sleep(0.5)
        mid(6,7)
        os.system('raspistill -t 1 -o 4.jpg')
        time.sleep(0.5)
        left_l(6,7)
        os.system('raspistill -t 1 -o 5.jpg')
        time.sleep(0.5)
        left_ll(6,7)
        os.system('raspistill -t 1 -o 6.jpg')
        time.sleep(0.5)
        mid(6,7)

        print("Sending ... ")
        
        os.system('echo "search" | mutt -s "search" -a "1.jpg" -- "a01043327120@gmail.com"')
        print("send mail")
        
    elif(dir==8):

        mid(0,15)
        time.sleep(0.05)
        
        
        
        
bus = smbus.SMBus(1)
address = 0x40

try:
    bus.write_byte_data(address,PCA9685_MODE1,0)
    set_PWMFreq(50)
    set_PWM(0,0,2048)
except IOError:
    print ("Perhaps there's no i2c device, run i2cdetect -y 1 for device connection!")
    pass

start_x=0
start_y=0
i=0
sw='0'
#sw=0 #first price
dist=distance_val()
print("welcom snake world!")

try:
    while True:
        
        sw=sw_val() # output sw func. value
        print(sw,dist)
        time.sleep(0.5)
    

        #if(sw == '7'): #manual    #수동조작        
        if(sw == '2'):#left:
            move(2) #turn left
            f = open('sw.txt', 'w')
            f.write('9') # stop
            f.close()
            

        elif(sw=='4'):#right):
            move(3) #turn right
            f = open('sw.txt', 'w')
            f.write('9') # stop
            f.close()

        elif(sw=='3'):#go):
            while True:
                dist=distance_val()
                move(1) #go

                if(dist == '0'):
                    move(5) #move left
                    
                
                sw=sw_val() # output sw func. value
                if(sw != '3'):
                    break
                
                    
        elif(sw=='9'):#stop):
            move(8)
            sw=sw_val() # output sw func. value
                    
        elif(sw=='0'):#light):
            GPIO.output(14,True)#LED On

        elif(sw=='1'):#light):
            GPIO.output(14,False)#LED Off

        elif(sw=='5'):
            print("Sending ...")
            time.sleep(0.5)
            os.system('echo "capture" | mutt -s "capture" -a "still_shot.jpg" -- "a01043327120@gmail.com"')
            time.sleep(0.05)
            print("Send complete")
            f = open('sw.txt', 'w')
            f.write('9') # stop
            f.close()
            
        elif(sw=='6'):#cam):
            
            left(5,6) #head up
            os.system('raspistill -t 1 -o still_shot.jpg&')
            time.sleep(0.05)
            print("cam capture")
        
            f = open('sw.txt', 'w')
            f.write('9') # stop
            f.close()


            #elif(sw=='8'):#auto):
                #sw==auto
         

        elif(sw == '8'):#auto):   #자동조작
            end_x=input('x 좌표를 입력하시오 :')
            end_y=input('y 좌표를 입력하시오 :')
            print("moving ... ","(",start_x," , ",start_y,")"," to ","(",end_x," , ",end_y,")")
            print("Start??")
            sw=input(sw_val())
            if(sw == '7'):#manual): #수동조작
                move(8)   #변수설정 
               
            elif(start_x==start_y and end_x==end_y):
                dist=distance_val()
                if(dist == '0'):
                    move(4) # move right
                    for i in range (0,6):
                        move(1) # move go
                    move(5) # move left

                else:
                    move(3) #left 30 deg ->  45deg   x
                    for i in range (0,6):
                        move(1) # move go
                    move(3) #turn left 30 deg ->  45deg   x
                    start_x=end_x
                    start_y=end_y
                
                f = open('sw.txt', 'w')
                f.write('9') # stop
                f.close()

            elif(start_x != end_x and start_y == end_y):

                if(start_x == start_y):
                    dist=distance_val()    

                    if(distance =='0'):
                        move(4) # move right
                        for i in range (0,6):
                            move(1) # move go
                        move(5) # move left

                    else:
                        for i in range (0,6):
                            move(1) # move go
                        for i in range (0,6):
                            move(2) # turn 180 left
                        start_x=end_x
                        start_y=end_y

                elif(start_x != start_y):
                    dist=distance_val()

                    if(distance < 30):
                        move(4) # move right
                        for i in range (0,6):
                            move(1) # move go
                        move(5) # move left

                    else:
                        for i in range (0,3):
                            move(2) #turn right 90 deg
                        for i in range (0,6):
                            move(1) # move go
                        for i in range (0,3):
                            move(3) #turn left 90 deg
                        start_x=end_x
                        start_y=end_y

                f = open('sw.txt', 'w')
                f.write('9') # stop
                f.close()    

            elif(start_x != end_x and start_y != end_y):

                dist=distance_val()

                if(distance == '0'):
                    move(4) # move right
                    for i in range (0,6):
                        move(1) # move go
                    move(5) # move left

                else:
                    move(2)#right 45 deg
                    for i in range (0,6):
                        move(1) #go_straight
                    move(2)#turn right 45 deg
                    start_x=end_x
                    start_y=end_y

                f = open('sw.txt', 'w')
                f.write('9') # stop
                f.close()
                
            elif(start_x == end_x and start_y != end_y):

                
                if(start_x == start_y):
                    dist=distance_val()
                    if(distance == '0'):
                        move(4) # move right
                        for i in range (0,6):
                            move(1) # move go
                        move(5) # move left

                    else:
                        for i in range (0,3):
                            move(3) #turn left 90 deg
                        for i in range (0,6):
                            move(1) # move go
                        for i in range (0,3):
                            move(2) #turn right 90 deg
                        start_x=end_x
                        start_y=end_y

                elif(start_x != start_y):
                    dist=distance_val()
                    if(distance =='0'):
                        move(4) # move right
                        for i in range (0,6):
                            move(1) # move go
                        move(5) # move left

                    else:
                        for i in range (0,3):
                            move(2) #turn right 90 deg
                        for i in range (0,6):
                            move(1) # move go
                        for i in range (0,3):
                            move(3) #turn left 90 deg
                        start_x=end_x
                        start_y=end_y


                f = open('sw.txt', 'w')
                f.write('9') # stop
                f.close()
    

except KeyboardInterrupt:
    
    print ("Servo driver Application End")
    set_PWM(0,0,0)
    GPIO.cleanup()

GPIO.cleanup()
 
