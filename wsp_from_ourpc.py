#import pyautogui
#import webbrowser
# from selenium import webdriver
import time, os
import pywhatkit
from datetime import datetime, timedelta
import argparse

parser=argparse.ArgumentParser(description='nombre de la imagen')
parser.add_argument('img')
args=parser.parse_args()

numero_telefonicos=("+51930266310",)#"+51969316575")

def send_wsp(img_name):
	ruta_imagen=os.getcwd()+r'/captures_img/{}.jpg'.format(str(img_name))#r'D:\PROYECTOS_PY\deteccion_movimento_camara_seguridad\v1\development\captures_img\imagen_rec.jpg'

	#url='https://web.whatsapp.com/send?phone='
	mensaje="Alerta de movimiento!,\n verificar imagen de camaras\n de seguridad"

	#enviar archivos adjuntos con pywhatkit
	for numero in numero_telefonicos:
		pywhatkit.sendwhats_image(numero, ruta_imagen,mensaje, wait_time = 5)
		time.sleep(2)
	#envio de mensajes con pywhatkit a grupos de whatsapp
	# pywhatkit.sendwhatmsg_to_group("ID_GROUP",mensaje,datetime.now().hour,
	# 								datetime.now().minute+1,
	# 								wait_time = 1,close_time = 1)

send_wsp(args.img)