# -*-coding: utf-8 -*-
rtsp_pre=None
def Hikvision(user, password, ip, num):
	#disponible tambien para la marca TrueVision
	rtsp = "rtsp://" + user.get() + ":" + password.get() + "@"+ ip.get() +":554/Streaming/channels/" + str(num) + "01"
	print (rtsp)
	return rtsp

def Dahua(user, password, ip, num):
	rtsp = "rtsp://" + user.get() + ":" + password.get() + "@"+ ip.get() +r":554/cam/realmonitor?channel=" + str(num) + r"&subtype=1"
	print (rtsp)
	return rtsp

def Uniview(user, password, ip, num):
	# Disponible para NVR
	rtsp = "rtsp://" + user.get() + ":" + password.get() + "@"+ ip.get() +":554/unicast/c" + str(num) + "/s0/live"
	print(rtsp)
	return rtsp

def Idis(user, password, ip, num):
	# Disponible para NVR
	rtsp = "rtsp://" + user.get() + ":" + password.get() + "@"+ ip.get() +":554/trackID=" + str(num)
	print(rtsp)
	return rtsp

def Samsung_HanwhaTechwin(user, password, ip, num):
	# Disponible para NVR
	rtsp = "rtsp://" + user.get() + ":" + password.get() + "@"+ ip.get() +":554/" + str(num-1)+"/profile1/media.smp"
	print(rtsp)
	return rtsp

def Annke(user, password, ip, num):
	rtsp = "rtsp://" + user.get() + ":" + password.get() + "@"+ ip.get() +":554/Streaming/Unicast/channels/" + str(num) + "01"
	print(rtsp)
	return rtsp

def webcam():
	rtsp = 0
	return rtsp

def top_lvl_otros():
	from tkinter import Toplevel, Label, StringVar, Button, Entry
	global ventana, e_otro
	def destroy_otros():
		global ventana, e_otro, rtsp_pre
		from tkinter import messagebox
		answer=messagebox.askyesno("Confirmar URL", "¿Deseas onfirmar?")
		if (answer):
			ventana.quit()
			rtsp_pre = e_otro.get()
			ventana.update()
	ventana=Toplevel()#Tk()
	ventana.title('Ingresar URL')
	ventana.iconbitmap(r"icons\camera1.ico")
	ventana.geometry('500x80')
	# Creacion de Widgets
	# Etiquetas
	label_nombre = Label(ventana,text="URL:  ",fg="#186cf7", font= ('Helvetica', 10, 'bold'),bg="#0a0a0a")
	label_nombre.grid(column=1, row=1, pady=5)#, columnspan = 2)
	# Entrys
	e_otro = StringVar(ventana, value="rtsp://")
	Entry_nombre = Entry(ventana, textvariable=e_otro, width=50, justify='left')#, validate="key")
	Entry_nombre.grid(column=3, row=1, padx=5, pady=5, columnspan = 3)
	# Botones
	btnAdd = Button(ventana,text="Aceptar",width=20, command=destroy_otros)
	btnAdd.grid(column=2, row=3, padx=5, pady=5, columnspan = 2)
	ventana.configure(background="#0a0a0a")
	ventana.mainloop()
	# return rtsp
def otros():
	global e_otro, rtsp_pre
	top_lvl_otros()
	#print ("r: "+ rtsp_pre)
	#return rtsp
def otros_return():
	global rtsp_pre
	print (rtsp_pre)
	return rtsp_pre