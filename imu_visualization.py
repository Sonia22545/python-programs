from vpython import *
import time
import numpy as np
import math
import serial
ser = serial.Serial('COM16',baudrate = 57600,timeout = 1)
time.sleep(2)
numpoints = 5
dataList = [0]*numpoints

def default():

    roll=0
    pitch=0
    yaw=0

def getValues():
    try:
        arduinoData = ser.readline().decode('ascii').split(',')
        return(arduinoData)
    except UnicodeDecodeError:
        arduinoData = ser.readline().decode('utf-8').split(',')
    return arduinoData



scene.range= 5 # setting the screen size
toRad =( np.pi/180 )# convert to radians
toDeg =( 180/np.pi )# convert to degrees
scene.forward = vector(-1,-1,-1)

scene.width = 600
scene.height = 600

xarrow = arrow(length=2,shaftwidth=.1,color=color.red,axis=vector(1,0,0)) #creating a reference arrow in the x direction
yarrow = arrow(length=2,shaftwidth=.1,color=color.green,axis=vector(0,1,0))#creating a reference arrow in the Y direction
zarrow = arrow(length=2,shaftwidth=.1,color=color.blue,axis=vector(0,0,1))#creating a reference arrow in the Z direction
frontArrow = arrow(length=4,shaftwidth=.1,color=color.purple,axis=vector(1,0,0))
upArrow = arrow(length=4,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0)) # magenta means pink as pink                                                                                  is not recognized
sideArrow = arrow(length=4,shaftwidth=.1,color=color.orange,axis=vector(0,0,1))

bBoard = box(length = 10,width=3,height=.3,opacity=.5)
uno =   box(length =3 ,width=1.8,height =.5,pos = vector(-3.3,.2,0),color=color.green)
mpu6050= box(length=1.2,width = 0.8,height=.2,pos = vector(-1,.2,0),color=color.blue)
myObj=compound([bBoard,uno,mpu6050]) # creating a common object for the mentioned so that we can animate it                                        together



while (1):

    for i in range(0,numpoints):
        data = getValues()
        dataList[i]= data
        #data = data.split(',')
        try:

            roll = float(data[0])*toRad
            pitch = float(data[1])*toRad
            yaw = float(data[2])*toRad+np.pi
            #print(x,y,z)
        except (IndexError,ValueError):

            default()
    rate(200)



    #my_roll_text  = f'ROLL= {roll}'
    #my_pitch_text = f'PITCH = {pitch}'
    #my_yaw_text   = f'YAW = {yaw}'

   # roll_label = label(text =my_roll_text,pos = vector(-5,5.5,0),color=color.red,box=False)
    #pitch_label = label(text =my_pitch_text,pos = vector(-5,5.0,0),color=color.blue,box=False)
    #yaw_label = label(text =my_yaw_text,pos = vector(-5,4.5,0),color=color.green,box=False)



    k = vector(cos(yaw)*cos(pitch),sin(pitch),sin(yaw)*cos(pitch)) # the hypotenuse vector for moving                                                                             the front arrow
    y=vector(0,1,0)# a reference vector for cross product
    s=cross(k,y) # cross product of vector K and Y to get the other orthogonal vector (for moving side                                                                                           arrow)
    v=cross(s,k) # cross product of vector s and k (for moving the up or front arrow )

    vrot =v*cos(roll) + cross(k,v)*sin(roll)

    frontArrow.axis=k # updating the axes
    sideArrow.axis=cross(k,vrot) #updating the axes
    upArrow.axis=vrot   #updating the axes

    myObj.axis=k # transferring the orientation to the object
    myObj.up=vrot   # declaring which side up



    frontArrow.length =4
    sideArrow.length=2
    upArrow.length=1
