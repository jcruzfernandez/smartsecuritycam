# -*-coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog, messagebox, Scale
import cv2, time
import imutils
from PIL import Image, ImageTk
import numpy as np
# from twilio.rest import Client 
from datetime import datetime, timedelta
from subprocess import Popen
from face_body_mediapipe import detect_body, detect_face
from face_body_tf import detect_body_tf
from select_model_rtsp import *
from database.db_email import toplevel_email
from database.db_whatsapp import toplevel_whatsapp
import threading, queue
#
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
iniciador=None
changeCamare=1
bgFondo1="#0a0a0a"
bglblVideo="#0a0a0a"
bgblue="#186cf7"
azul_cv2 = (255, 0, 0)
rojo_cv2 = (0, 0, 255)
verde_cv2 = (0, 255, 0)
q=queue.Queue()
# q2=queue.Queue()

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
executor=ThreadPoolExecutor(max_workers=8)
hilo=None
#Coordenadas iniciales de area vigilada
ix, iy = -1, -1
fx, fy = 0, 0
RTSP=""
funDVR_no=None

def iniciar():
    global cap
    global Time_1
    #cap = cv2.VideoCapture(0)
    # Time_1= datetime.now()
    #video()
    ret, frame=cap.read()
    if ret == True:
        frame = cv2.resize(frame, (640,360), interpolation = cv2.INTER_NEAREST)
        # frame=imutils.resize(frame, width=640)
        q.put(frame)
    # else:
    #     cap.release()

def make_picture(img):
    name=str(datetime.now()).split(".")[0]
    name=name.replace(" ","_")
    name=name.replace(":",".")
    picturefile=r'captures_img/{}.jpg'.format(name)
    cv2.imwrite(picturefile, img)
    return name

def video():
    global cap
    global Time_1
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # ret, frame=cap.read()
    # if ret == True:
    #     frame=imutils.resize(frame, width=640)
    try:
        hilo_f=executor.submit(iniciar())
    except:
        print ("reintentanto... ")
    if q.empty() !=True:
        frame=q.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Cuadro de advertencia en el frame que señala estado de movimiento
        #text_estado = "Estado: No se detecta movimiento"
        #area_vigilada configurada actualmente para toda la vista de la camara
        #ancho = frame.shape[1]
        #alto = frame.shape[0]
        CAV=coord_area_vigilada()
        area_vigilada=np.array([[CAV[0],CAV[1]],[CAV[2],CAV[1]],[CAV[2],CAV[3]],[CAV[0],CAV[3]]])
        # area_vigilada = np.array([[5,40],[ancho-5,40],[ancho-5,alto-5],[5,alto-5]])
        #q2.put(frame)
        if var_int.get()==3:
            # executor.submit(full_detection, q.get(),gray,area_vigilada)
            # frame=full_detection(frame,gray,area_vigilada)
            # if q.empty() !=True:
            hilo=executor.submit(full_detection, frame,gray,area_vigilada)
                # p1=threading.Thread(target=full_detection, args=(q.get(),gray,area_vigilada))
                # p1.start()
            # else:
            #     pass
            # p1.join()
        elif var_int.get()==2:
            # frame=detect_body(frame)
            hilo=executor.submit(detect_body_tf, frame, 0.60)
        elif var_int.get()==1:
            # frame=detect_face(frame)
            hilo=executor.submit(detect_face, frame)
        cv2.drawContours(frame, [area_vigilada], -1, verde_cv2, 2)
        #frame = cv2.resize(frame, (640,360), interpolation = cv2.INTER_NEAREST)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        lbl_video.configure(image=frame)
        lbl_video.image=frame
        #del hilo_f
        lbl_video.after(30,video)
    else:
        print ("error...conexión debil o lenta")
        if lbl_video.image!="":
            print("reintentando...")
            iniciar2()
        # #cap.release()

def iniciar2 ():
    global cap
    global Time_1
    global cam_no, iniciador
    iniciador=True
    rtsp = RTSP#"rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "01"
    if userdvr.get()=="" or passdvr.get()=="" or ipdvr.get()=="" or RTSP=="":
        messagebox.showinfo('Mensaje', 'Llene los campos: IP DVR, USER DVR, PASSWORD DVR\no\nEscoga Marca de DVR / NVR: Archivo -> Escoger Marca')
    else:
        Time_1= datetime.now()
        cap=cv2.VideoCapture(rtsp)
        if cap.isOpened():
            try:
                video()
            except:
                pass
            # video()
        else:
            print (rtsp)
            messagebox.showwarning('Alerta', 'Vinculo fallido...\n\nVerificar datos ingresados')
            cap=None #finalizar()

def finalizar():
    global cap
    if cap==None:
        pass
    else:
        lbl_video.image=""
        cap.release()
        textlblvideo.set("PAUSADO")
    root.bell()

def previo():
    global iniciador
    if iniciador == True:
        global cam_no
        global cap
        cap.release()
        cam_no=cam_no-1
        if (cam_no<1):
            cam_no=4
        lblcamActiva=Label(root,text="{}".format(cam_no), bg="#252525",
                            fg='white').grid(column=3, row=17,columnspan=1)
        exec('fun_dvr{}()'.format(funDVR_no))
        rtsp = RTSP#"rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "01"
        cap=cv2.VideoCapture(rtsp)
        try:
            video()
        except:
            pass
    else:
        messagebox.showinfo('Mensaje', 'Pulse INICIAR antes de seguir')

def siguiente():
    global iniciador, make_picture
    if iniciador == True:
        global cam_no, funDVR_no
        global cap
        cap.release()
        cam_no=cam_no+1
        if (cam_no>4):
            cam_no=1
        lblcamActiva=Label(root,text="{}".format(cam_no),bg="#252525",
                            fg='white').grid(column=3, row=17,columnspan=1)
        exec('fun_dvr{}()'.format(funDVR_no))
        rtsp = RTSP#"rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "01"
        cap=cv2.VideoCapture(rtsp)
        try:
            video()
        except:
            pass
    else:
        messagebox.showinfo('Mensaje', 'Pulse INICIAR antes de seguir')

def only_numeric_input_hora(P):
    # Verifica si el valor ingresado en los ENTRY son numericos o vacios y retorna un boleano
    if P == "" or len(P)<=2 and P.isdigit() and (0<=int(P)<=24 ):
        return True
    return False

def only_numeric_input_minuto(P):
    # Verifica si el valor ingresado en los ENTRY son numericos o vacios y retorna un boleano
    if P == "" or len(P)<=2 and P.isdigit() and (0<=int(P)<=60 ):
        return True
    return False

def face_detection(img,gray):
    f_face = frontalfaceClassif.detectMultiScale(gray, 1.1, 3)
    # p_face = profilefaceClassif.detectMultiScale(gray, 1.1, 3)
    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in f_face:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,255,0), 1)
    # for (x,y,w,h) in p_face:
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
    return img

def body_detection(img,gray):
    bodies = bodyClassif.detectMultiScale(gray, 1.2, 3)
    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in bodies:
        cv2.rectangle(img, (x, y), (x+w, y+h), (163, 73, 164), 1)
    return img

def full_detection(img,gray, area_vigilada):
    global Time_1, cap
    #Creacion de imagen Auxiliar
    imgAux = np.zeros(shape=img.shape[:2],dtype=np.uint8)
    imgAux = cv2.drawContours(imgAux,[area_vigilada],-1,(255),-1)
    img_area = cv2.bitwise_and(gray, gray, mask=imgAux)

    fgmask = fgbg.apply(img_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)
    contours = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for contour in contours:
        if 15000 > cv2.contourArea(contour) > var_slide.get(): #1000:
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w,y+h), (0, 0, 255), 2)
            text_estado = "Estado: !Alerta de movimiento!"
            color = (0, 0, 255)
            if datetime.now()>Time_1:
                # cv2.drawContours(img,[area_vigilada], -1, color, 2)
                timedelta_activacion=datetime.now()
                try:
                    Time_1 = datetime.now() + timedelta(seconds=12)
                    name=make_picture(img)
                    # Popen('python3 send_email.py {}'.format(name), shell=False)
                    # Popen('python3 alarm_sound.py', shell=False)
                    # Popen('python3 wsp_from_ourpc.py {}'.format(name), shell=False)
                    #Twilio()
                except:
                    print ("ERROR")
        else:
            pass
    cv2.drawContours(img,[area_vigilada], -1, (0, 255, 0), 2)
    return img
    # q2.put(img)

def salir_tk():
    answer=messagebox.askyesno("Salir", "¿Deseas salir?")
    if (answer):
        root.destroy()

def coord_area_vigilada():
    global ix, iy, fx, fy
    if ix==-1:
        ix, iy, fx, fy=1, 1, 639, 359
    return ix, iy, fx, fy

drawing = False
# if True, draw rectangle. Press 'm' to toggle to curve
mode = True 
# mouse callback function
def draw_shape_b1(event):
    global ix, iy, drawing, fx, fy
    drawing = True
    ix, iy = event.x, event.y

def draw_shape_Mb1(event):
    global ix, iy, drawing, fx, fy
    if drawing == True:
        fx, fy= event.x, event.y

def draw_shape_Rb1(event):
    global ix, iy, drawing, fx, fy
    drawing = False
    fx, fy= event.x, event.y
    answer=messagebox.askyesno(" ", "¿Confirmar area?")
    if (answer):
        cap.release()

def draw_box():
    global mode, fx, fy, ix, iy, cap

    #cap=cv2.VideoCapture(rtsp)
    hilo_f=executor.submit(iniciar())
    if q.empty() != True:
        frame=imutils.resize(q.get(), width=640)
        cv2.rectangle(frame, (ix, iy), (fx, fy), (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        lbl_video.configure(image=frame)
        lbl_video.image=frame
        lbl_video.after(10,draw_box)
    # ret, frame=cap.read()
    # if ret == True:
    #     frame=imutils.resize(frame, width=640)
    #     cv2.rectangle(frame, (ix, iy), (fx, fy), (0, 255, 0), 2)
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     frame = Image.fromarray(frame)
    #     frame = ImageTk.PhotoImage(image=frame)
    #     lbl_video.configure(image=frame)
    #     lbl_video.image=frame
    #     lbl_video.after(10,draw_box)
    else:
        #lbl_video.image=""
        cap.release()
    # #return  (ix, iy, fx, fy)

def alerta_box():
    global cap, fx, fy, ix, iy
    global cam_no
    rtsp = RTSP#"rtsp://" + userdvr.get() + ":" + passdvr.get() + "@"+ ipdvr.get() +":554/Streaming/channels/" + str(cam_no) + "01"
    if userdvr.get()=="" or passdvr.get()=="" or ipdvr.get()=="" or RTSP=="":
        messagebox.showinfo('Mensaje', 'Llene los campos: IP DVR, USER DVR, PASSWORD DVR\no\nEscoga Marca de DVR / NVR: Archivo > Escoger Marca')
    else:
        cap=cv2.VideoCapture(rtsp)
        if cap.isOpened():
            draw_box()
            #lbl_video.bind('<Button-1>', cv2.setMouseCallback("windowName", draw_shape))
            lbl_video.bind('<Button-1>', draw_shape_b1)
            lbl_video.bind('<B1-Motion>',draw_shape_Mb1)
            lbl_video.bind('<ButtonRelease-1>', draw_shape_Rb1)
            #else:
                #messagebox.showinfo('Mensaje', '!Area de Vigilancia asignada!')
        else:
            messagebox.showwarning('Alerta', 'Vinculo fallido...\n\nVerificar datos ingresados')
            cap=None

def fun_dvr1():
    global RTSP, cam_no, funDVR_no
    RTSP=Hikvision(userdvr,passdvr,ipdvr, cam_no)
    funDVR_no=1
    btnPrevio['state']=NORMAL
    btnSiguiente['state']=NORMAL
def fun_dvr2():
    global RTSP, cam_no, funDVR_no
    RTSP=Dahua(userdvr,passdvr,ipdvr, cam_no)
    funDVR_no=2
    btnPrevio['state']=NORMAL
    btnSiguiente['state']=NORMAL
def fun_dvr3():
    global RTSP, cam_no, funDVR_no
    RTSP=Uniview(userdvr,passdvr,ipdvr, cam_no)
    funDVR_no=3
    btnPrevio['state']=NORMAL
    btnSiguiente['state']=NORMAL
def fun_dvr4():
    global RTSP, cam_no, funDVR_no
    RTSP=Idis(userdvr,passdvr,ipdvr, cam_no)
    funDVR_no=4
    btnPrevio['state']=NORMAL
    btnSiguiente['state']=NORMAL
def fun_dvr5():
    global RTSP, cam_no, funDVR_no
    RTSP=Samsung_HanwhaTechwin(userdvr,passdvr,ipdvr, cam_no)
    funDVR_no=5
    btnPrevio['state']=NORMAL
    btnSiguiente['state']=NORMAL
def fun_dvr6():
    global RTSP, cam_no, funDVR_no
    RTSP=Annke(userdvr,passdvr,ipdvr, cam_no)
    funDVR_no=6
    btnPrevio['state']=NORMAL
    btnSiguiente['state']=NORMAL
def fun_dvr7():
    global RTSP, cam_no, funDVR_no
    RTSP=webcam()
    funDVR_no=7
    btnPrevio['state']=DISABLED
    btnSiguiente['state']=DISABLED
def fun_dvr8():
    global RTSP, cam_no, funDVR_no
    otros()
    RTSP=otros_return()
    funDVR_no=8
    btnPrevio['state']=DISABLED
    btnSiguiente['state']=DISABLED

cap=None
cam_no=1
#Ventana general
root= Tk()
root.title("Sistema de alarma")
root.iconbitmap(r"icons\camera4.ico")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_width = 1000
root_height = 750
# buscando centro de pantalla
center_x = int(screen_width/2 - root_width/2)
center_y = int(screen_height/2 - root_height/2)
root.geometry(f'{root_width}x{root_height}+{center_x}+{center_y}')

#Etiquetas y texto de entradas de DVR
ipdvr = StringVar(root,value="190.238.0.250")
lbl_IPDVR = Label(root,text="IP DVR:",bg=bgFondo1,fg='white').grid(column=0,row=1,columnspan=4)
Entry_IPDVR = Entry(root, textvariable=ipdvr,width=20,justify='center').grid(column=0,row=2,columnspan=4)

userdvr = StringVar(root,value='admin')
lbl_USERDVR = Label(root,text="USER DVR:",bg=bgFondo1,fg='white').grid(column=0,row=3,columnspan=4)
Entry_USERDVR = Entry(root, textvariable=userdvr,width=20,justify='center').grid(column=0,row=4,columnspan=4)

passdvr = StringVar(root,value="milkit@261113")
lbl_CLAVEDVR = Label(root,text="PASSWORD DVR:",bg=bgFondo1,fg='white').grid(column=0,row=5,columnspan=4)
Entry_CLAVEDVR = Entry(root, textvariable=passdvr,width=20,justify='center', show="*").grid(column=0,row=6,columnspan=4)

# Creacion de barra MENU 
barraMenu=Menu(root, bg='blue', fg='white')  # barra de menu principal
# componentes de la barra de Menu
menuArchivo=Menu(barraMenu, tearoff=0)
menuHerramienta = Menu(barraMenu, tearoff=0)
menuAyuda = Menu(barraMenu)

# Falsa barra de titulo
title_bar = Frame(root, relief="raised", bd=1)
title_bar.grid(column=0, row=0)

#Agregar SUBMENU a "Archivo"
sub_menuArchivo = Menu(menuArchivo,tearoff=0)
# Agregando Comandos a los Menus y Submenus
menuArchivo.add_cascade(label="Elegir marca", menu=sub_menuArchivo)
sub_menuArchivo.add_command(label="Hikvision",command=fun_dvr1)
sub_menuArchivo.add_command(label="Dahua",command=fun_dvr2)
sub_menuArchivo.add_command(label="Uniview",command=fun_dvr3)
sub_menuArchivo.add_command(label="Idis",command=fun_dvr4)
sub_menuArchivo.add_command(label="Samsung/HanwhaTechwin", command=fun_dvr5)
sub_menuArchivo.add_command(label="Annke",command=fun_dvr6)
sub_menuArchivo.add_command(label="Webcam",command=fun_dvr7)
sub_menuArchivo.add_command(label="Otros",command=fun_dvr8)
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir", command=salir_tk)
menuHerramienta.add_command(label="Alerta por Email", command=toplevel_email)
menuHerramienta.add_command(label="Alerta por WhatsApp", command=toplevel_whatsapp)
menuHerramienta.add_command(label="Area de Vigilancia",command=alerta_box)
menuAyuda.add_command(label="Informacion")
menuAyuda.add_command(label="Soporte")

# Agregar MENUS a la barra
barraMenu.add_cascade(label="Archivo", menu=menuArchivo)
barraMenu.add_cascade(label="Herramientas", menu=menuHerramienta)
barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
barraMenu.add_command(label="Salir", command=salir_tk)


#Creacion de Widgets
#Etiqueta inicial
lbl_1=Label(root,text="Establesca parametros:",
            bg=bgFondo1,fg="#186cf7",height=35,
            font= ('Helvetica', 11, 'bold'))
lbl_1.grid(column=0, row=0, padx=10, pady=10,columnspan=4)

# Frame y FrameLabel de video
Frame_video_lbl=LabelFrame(root,text=" Area de Video ", padx=1, pady=1, bg=bglblVideo, fg=bgblue, font= ('Helvetica', 9, 'bold'))
Frame_video_lbl.grid(column=4, row=0, rowspan=21, sticky="nsew",padx=10,pady=10)
Frame_video = Frame(Frame_video_lbl,bg=bgFondo1,width=650, height=500)
Frame_video.grid(column=0, row=0, sticky="nsew")
#Etiqueta de video dentro EtiquetaFRAME
textlblvideo=StringVar()
lbl_video=Label(Frame_video_lbl,text="NO VIDEO",bg=bgFondo1,fg="#186cf7", textvariable=textlblvideo)
# lbl_video.grid(column=0, row=0, sticky="nsew")
lbl_video.place(x=0, y=0)

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
callback_hora=root.register(only_numeric_input_hora)
callback_min=root.register(only_numeric_input_minuto)
#Widgets de input hora y minutos ini/fin
horaInicio=StringVar(root, value="00")
minutoInicio=StringVar(root, value="00")
entryHoraInicio=Entry(root, textvariable=horaInicio, width=5,justify='center',
                    validate="key", validatecommand=(callback_hora, '%P')).grid(column=1,row=8)
entryMinutoInicio=Entry(root, textvariable=minutoInicio, width=5,justify='center',
                    validate="key", validatecommand=(callback_min, '%P')).grid(column=3,row=8)

horaFin=StringVar(root, value="00")
minutoFin=StringVar(root, value="00")
entryHoraFin=Entry(root, textvariable=horaFin, width=5,justify='center',
                    validate="key", validatecommand=(callback_hora, '%P')).grid(column=1,row=10)
entryMinutoFin=Entry(root, textvariable=minutoFin, width=5,justify='center',
                    validate="key", validatecommand=(callback_min, '%P')).grid(column=3,row=10)

#RadioBotton
# var_face, var_body, var_all=IntVar(), IntVar(), IntVar()
var_int=IntVar()
lblModo=Label(root,text="Modo de deteccion: ",bg=bgFondo1,fg=bgblue,justify='left').grid(column=0, row=11,columnspan=4, pady=5)
rdBfacedetection=Radiobutton(root, text="Detectar rostros", bg=bgFondo1,fg=bgblue,value=1, variable=var_int)
rdBfacedetection.grid(column=0,row=12,columnspan=4)
rdBbodydetection=Radiobutton(root, text="Detectar personas", bg=bgFondo1,fg=bgblue,value=2, variable=var_int)
rdBbodydetection.grid(column=0,row=13,columnspan=4)
rdBfulldetection=Radiobutton(root, text="Detectar cualquier movimiento", bg=bgFondo1,fg=bgblue,value=3, variable=var_int)
rdBfulldetection.grid(column=0,row=14,columnspan=4)
rdBfulldetection.select()
# Barra deslisable
var_slide=IntVar()
SclBar=Scale(root, label="Sensibilidad", orient=HORIZONTAL,bg=bgFondo1,fg=bgblue, tickinterval=1000,
            length=300, from_=0, to=5000, variable=var_slide)
SclBar.grid(column=0,row=16,columnspan=4, pady=10, padx=10)
SclBar.set(1500)

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

btnFinalizar =Button(root,text="Pausar",width=10, command=finalizar)
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
root.config(menu=barraMenu)
#root.iconify()
#root.attributes('-alpha',0.5)
root.mainloop()

