#!/usr/bin/env python
# coding: utf-8

import cv2
import os
import numpy as np
from twilio.rest import Client 
import time
from datetime import datetime, timedelta
#from send_email import *
#from alarm_sound import *
from subprocess import Popen

#cap = cv2.VideoCapture('videos_de_prueba/cabina_asaltada_reso360p_cortado.mp4')
# cap = cv2.VideoCapture(0)
# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

def Twilio():
    account_sid = 'ACf86e3a143943c07d272a449b0a47ae59'#os.environ[]
    auth_token = '850b9128f7732f8bb10a2f63bb22c783'#os.environ[]
    client = Client(account_sid, auth_token) 
 
    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Alerta de movimiento  \n Llamar al 105',      
                              to='whatsapp:+51955762637' 
                              ) 
    # message2 = client.messages.create( 
                              # from_='+16163742019',  
                              # body='Alerta de movimiento',      
                              # to='+51966234648' 
                              # ) 
    # message3 = client.messages.create( 
    #                           from_='+16163742019',  
    #                           body='Alerta de movimiento \n Llamar al 105',      
    #                           to='+519' 
    #                           ) 
    message4 = client.messages.create( 
                              from_='+16163742019',  
                              body='Alerta de movimiento\n Llamar al 105',      
                              to='+51954643400' 
                              ) 
    print(message.sid)

def detection():
    cap = cv2.VideoCapture(0)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    Time_1= datetime.now()
    #Time_2= datetime.now()+ timedelta(seconds=1)
    while True:
        ret, frame  = cap.read()
        if ret == False:
         break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #Cuadro de advertencia en el frame que señala estado de movimiento
        cv2.rectangle(frame,(0,0),(frame.shape[1],40),(0,0,0),-1)
        color= (0,255,0)
        text_estado = "Estado: No se detecta movimiento an AREA"
        #area_vigilada configurada actualmente para toda la vista de la camara
        ancho = frame.shape[1] 
        alto = frame.shape[0]
        #area_vigilada= np.array([[5,40],[ancho-5,40],[ancho-5,alto-5],[5,alto-5]])
        area_vigilada= np.array([[5,40],[ancho-5,40],[ancho-5,alto-5],[5,alto-5]])
        
        #Creacion de imagen Auxiliar
        imgAux = np.zeros(shape=frame.shape[:2],dtype=np.uint8)
        imgAux = cv2.drawContours(imgAux,[area_vigilada],-1,(255),-1)
        img_area = cv2.bitwise_and(gray, gray, mask=imgAux)
        
        fgmask = fgbg.apply(img_area)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.dilate(fgmask, None, iterations=2)
        
        contours = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for contour in contours:
            if cv2.contourArea(contour)> 1200:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
                text_estado = "Estado: !Alerta de movimiento!"
                color = (0,0,255)
                #a = datetime.now()

                if datetime.now()>Time_1:
                    try:
                        Time_1 = datetime.now() + timedelta(seconds=12)
                        #email()
                        #Popen('python3 send_email.py', shell=False)
                        Popen('python3 alarm_sound.py', shell=False)
                        #Popen('python3 wsp_from_ourpc.py', shell=False)
                        #Twilio()
                    except:
                        pass
                #time.sleep(0.5)
        cv2.drawContours(frame,[area_vigilada], -1, color, 2)
        cv2.putText(frame, text_estado, (10,30), cv2.FONT_HERSHEY_SIMPLEX,1, color,2)
        cv2.imshow('frame', frame)
        cv2.imshow('fgmask', fgmask)
        k= cv2.waitKey(25) & 0xFF
        if k== 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    #return (frame,cap)
detection()