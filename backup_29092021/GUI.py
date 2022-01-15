from tkinter import *
from tkinter import filedialog, messagebox
import cv2, os
import imutils
from PIL import Image, ImageTk
import numpy as np
from twilio.rest import Client 
import time
from datetime import datetime, timedelta
from subprocess import Popen

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
iniciador=None
changeCamare=1
bgFondo1="#0a0a0a"
bglblVideo="#0a0a0a"
bgblue="#186cf7"

def iniciar():
    global cap
    global Time_1
    cap = cv2.VideoCapture(0)
    Time_1= datetime.now()
    video()

def make_picture(img):
    name=str(datetime.now()).split(".")[0]
    print (name)
    picturefile=r"captures_img\{}.jpg".format(name.replace(":","_"))
    cv2.imwrite(picturefile, img)
    #print ("Foto tomada")

def video():
    global cap
    global Time_1
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #Time_1= datetime.now()
    # Time_2= datetime.now()+ timedelta(seconds=1)
    # while True:
    #cap.set(3, 1280)  # ID number for width is 3
    #cap.set(4, 960)
    ret, frame=cap.read()
    if ret == True:
        frame=imutils.resize(frame, width=700)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Cuadro de advertencia en el frame que señala estado de movimiento
        cv2.rectangle(frame, (0,0), (frame.shape[1], 40), (0,0,0), -1)
        color= (0,255,0)
        text_estado = "Estado: No se detecta movimiento"
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
            if cv2.contourArea(contour) > 1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 0, 255), 2)
                text_estado = "Estado: !Alerta de movimiento!"
                color = (0, 0, 255)
                
                if datetime.now()>Time_1:
                    try:
                        Time_1 = datetime.now() + timedelta(seconds=12)
                        make_picture(frame)
                        #Popen('python3 send_email.py', shell=False)
                        Popen('python3 alarm_sound.py', shell=False)
                        #Popen('python3 wsp_from_ourpc.py', shell=False)
                        #Twilio()
                    except:
                        print ("ERROR")
            else:
                pass
                #time.sleep(0.5)
        cv2.drawContours(frame,[area_vigilada], -1, color, 2)
        cv2.putText(frame, text_estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        lbl_video.configure(image=frame)
        lbl_video.image=frame
        lbl_video.after(10,video)
    else:
        lbl_video.image=""
        cap.release()

def iniciar2 ():#user, password, ip, channel):
    global cap
    global Time_1
    global cam_no, iniciador
    iniciador=True
    rtsp = "rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "02"
    if userdvr.get()=="" or passdvr.get()=="" or ipdvr.get()=="":
        messagebox.showinfo('Mensaje', 'LLENAR LOS CAMPOS:\n\t\t\tIP DVR\n\t\t\tUSER DVR\n\t\t\tPASSWORD DVR')
    else:
        Time_1= datetime.now()
        cap=cv2.VideoCapture(rtsp)
        if cap.isOpened():
            print (rtsp)
            video()
        else:
            print (rtsp)
            messagebox.showwarning('Alerta', 'Vinculo fallido...\n\nVerificar datos ingresados')
            cap=None #finalizar()
    #print (rtsp)

def finalizar():
    global cap
    if cap==None:
        pass
    else:
        cap.release()
    root.bell()

def previo():
    global iniciador
    if iniciador==True:
        global cam_no
        global cap
        cap.release()
        cam_no=cam_no-1
        if (cam_no<1):
            cam_no=4
        lblcamActiva=Label(root,text="{}".format(cam_no), bg="#252525",
                            fg='white').grid(column=3, row=17,columnspan=1)
        #del cap
        rtsp = "rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "01"
        cap=cv2.VideoCapture(rtsp)
        #time.sleep(1)
        video()
    else:
        messagebox.showinfo('Mensaje', 'Pulse INICIAR antes de seguir')
    #root.update()
    #return cam_no

def siguiente():
    global iniciador, make_picture
    if iniciador==True:
        global cam_no
        global cap
        cap.release()
        cam_no=cam_no+1
        if (cam_no>4):
            cam_no=1
        lblcamActiva=Label(root,text="{}".format(cam_no),bg="#252525",
                            fg='white').grid(column=3, row=17,columnspan=1)
        #del cap
        rtsp = "rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "01"
        cap=cv2.VideoCapture(rtsp)
        #time.sleep(1)
        video()
    else:
        messagebox.showinfo('Mensaje', 'Pulse INICIAR antes de seguir')
    #root.update()
    #return cam_no

def only_numeric_input(P):
    #Verifica si el valor ingresado en los ENTRY son numericos o vacios y retorna un boleano
    if P == "" or len(P)<=2 and P.isdigit():
        return True
    return False

def face_detection(img):
    frontalfaceClassif = cv2.CascadeClassifier(r'\data_opencv\haarcascade_frontalface_default.xml')
    profilefaceClassif = cv2.CascadeClassifier(r'\data_opencv\haarcascade_profileface.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f_face = frontalfaceClassif.detectMultiScale(gray, 1.1, 3)
    p_face = profilefaceClassif.detectMultiScale(gray, 1.1, 3)
    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in f_face:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
    for (x,y,w,h) in p_face:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
    return img

def bady_detection(img):
    bodyClassif = cv2.CascadeClassifier(r'\data_opencv\haarcascade_fullbody.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bodies = bodyClassif.detectMultiScale(gray, 1.1, 3)
    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in bodies:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
    return img



    
cap=None
cam_no=1
#Ventana general
root= Tk()
root.title("Configuracion del sistema de alarma")
root.iconbitmap(r"icons\camera4.ico")
root.geometry("900x640")

#Creacion de Widgets
#Etiqueta inicial
lbl_1=Label(root,text="Establesca parametros:",
            bg=bgFondo1,fg="#186cf7",
            font= ('Helvetica', 11, 'bold'))
lbl_1.grid(column=0, row=0, padx=10, pady=10,columnspan=4)

#Etiquetas y texto de entradas de DVR
ipdvr = StringVar(root,value="190.238.88.82")
lbl_IPDVR = Label(root,text="IP DVR:",bg=bgFondo1,fg='white').grid(column=0,row=1,columnspan=4)
Entry_IPDVR = Entry(root, textvariable=ipdvr,width=20,justify='center').grid(column=0,row=2,columnspan=4)

userdvr = StringVar(root,value='admin')
lbl_USERDVR = Label(root,text="USER DVR:",bg=bgFondo1,fg='white').grid(column=0,row=3,columnspan=4)
Entry_USERDVR = Entry(root, textvariable=userdvr,width=20,justify='center').grid(column=0,row=4,columnspan=4)

passdvr = StringVar(root,value="milkit@261113")
lbl_CLAVEDVR = Label(root,text="PASSWORD DVR:",bg=bgFondo1,fg='white').grid(column=0,row=5,columnspan=4)
Entry_CLAVEDVR = Entry(root, textvariable=passdvr,width=20,justify='center', show="*").grid(column=0,row=6,columnspan=4)

# Frame y FrameLabel de video
Frame_video_lbl=LabelFrame(root,text=" Area de Video ", padx=1, pady=1, bg=bglblVideo, fg='white')
Frame_video_lbl.grid(column=4, row=0, rowspan=20, sticky="nsew",padx=10,pady=10)
Frame_video = Frame(Frame_video_lbl,bg=bgFondo1,width=650, height=500)
Frame_video.grid(column=0, row=0, sticky="nsew")
#Etiqueta de video dentro EtiquetaFRAME
lbl_video=Label(Frame_video_lbl,text="NO VIDEO",bg=bgFondo1,fg="#186cf7")
lbl_video.grid(column=0, row=0, sticky="nsew")

lblHoraInicio=Label(root,text="Fijar hora de Inicio",bg=bgFondo1,fg='white')
lblHoraInicio.grid(column=0, row=7, padx=10, pady=10,columnspan=4)

lblHoraFin=Label(root,text="Fijar hora de Fin",bg=bgFondo1,fg='white')
lblHoraFin.grid(column=0, row=9, padx=10, pady=10,columnspan=4)

# Widgets de ingreso de texto
#variables
lblHrIni=Label(root,text="HORA: ",bg=bgFondo1,fg='white').grid(column=0, row=8)
lblMinIni=Label(root,text="MIN: ",bg=bgFondo1,fg='white').grid(column=2, row=8)
lblHrFin=Label(root,text="HORA: ",bg=bgFondo1,fg='white').grid(column=0, row=10)
lblMinFin=Label(root,text="MIN: ",bg=bgFondo1,fg='white').grid(column=2, row=10)

#validacion de hora y minutos (solo numeros)
callback=root.register(only_numeric_input)
#Widgets de input hora y minutos ini/fin
horaInicio=StringVar(root, value="00")
minutoInicio=StringVar(root, value="00")
entryHoraInicio=Entry(root, textvariable=horaInicio,
                    width=5,justify='center',
                    validate="key", validatecommand=(callback, '%P')).grid(column=1,row=8)
entryMinutoInicio=Entry(root, textvariable=minutoInicio,
                    width=5,justify='center',
                    validate="key", validatecommand=(callback, '%P')).grid(column=3,row=8)

horaFin=StringVar(root, value="00")
minutoFin=StringVar(root, value="00")
entryHoraFin=Entry(root, textvariable=horaFin,
                    width=5,justify='center',
                    validate="key", validatecommand=(callback, '%P')).grid(column=1,row=10)
entryMinutoFin=Entry(root, textvariable=minutoFin,
                    width=5,justify='center',
                    validate="key", validatecommand=(callback, '%P')).grid(column=3,row=10)

#RadioBotton
var_face, var_body, var_all=IntVar(), IntVar(), IntVar()
lblModo=Label(root,text="Modo de deteccion: ",bg=bgFondo1,fg=bgblue,justify='left').grid(column=0, row=11,columnspan=4)
rdBfacedetection=Radiobutton(root, text="Detectar rostros", bg=bgFondo1,fg=bgblue,value=1, variable=var_face).grid(column=0,row=12,columnspan=4)
rdBbodydetection=Radiobutton(root, text="Detectar personas", bg=bgFondo1,fg=bgblue,value=2, variable=var_body).grid(column=0,row=13,columnspan=4)
rdBalldetection=Radiobutton(root, text="Detectar cualquier movimiento", bg=bgFondo1,fg=bgblue,value=3, variable=var_all).grid(column=0,row=14,columnspan=4)

#Barra deslisable
var_slide=IntVar()
SclBar=Scale(root, label="Presicion", orient=HORIZONTAL,bg=bgFondo1,fg=bgblue, tickinterval=500,
            length=300, from_=500, to=2500, variable=var_slide).grid(column=0,row=16,columnspan=4)
#SclBar.set(state=DISABLED)

#Etiqueta: camara activa
lblcamera=Label(root,text="Deteccion en camara N° ",bg=bgFondo1,fg='white').grid(column=0, row=17,columnspan=3)
lblcamActiva=Label(root,text="{}".format(cam_no),bg=bgFondo1,fg='white').grid(column=3, row=17,columnspan=1)
#Botones PREVIO / SIGUIENTE
btnPrevio =Button(root,text="<< Previo",width=10, command=previo)
btnPrevio.grid(column=0, row=18, padx=5, pady=5,columnspan=2)

btnSiguiente =Button(root,text=" Siguiente >> ",width=10, command=siguiente)
btnSiguiente.grid(column=2, row=18, padx=5, pady=5,columnspan=2)

btnIniciar =Button(root,text="Iniciar",width=10, command=iniciar2)
btnIniciar.grid(column=0, row=20, padx=5, pady=5,columnspan=2)

btnFinalizar =Button(root,text="Finalizar",width=10, command=finalizar)
btnFinalizar.grid(column=2, row=20, padx=5, pady=5,columnspan=2)

# Configuracion de ventana adaptativa
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root,4, weight=1)

# Configuracion adaptavia de video
#Grid.rowconfigure(lbl_video, 0, weight=1)
#Grid.columnconfigure(lbl_video, 0, weight=1)
Grid.rowconfigure(Frame_video_lbl, 0, weight=1)
Grid.columnconfigure(Frame_video_lbl,0, weight=1)

#Configuracion de Widgets
root.configure(background=bgFondo1)
#root.wm_state('iconic')
#root.iconify()
root.mainloop()

