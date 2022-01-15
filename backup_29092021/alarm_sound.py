# -*- coding: utf-8 -*-
from playsound import playsound
import os

def play_alarm():
	root=os.getcwd()
	file=os.path.join(str(root),r"sounds\alarm_3.mp3")
	#print (file)
	#file=
	playsound(file)
# path=r'D:\PROYECTOS_PY\deteccion_movimento_camara_seguridad\v1\development\sounds\sound_alarm_2.mp3'
# print (path)
play_alarm()

#D:\PROYECTOS_PY\deteccion_movimento_camara_seguridad\v1\development\sounds
#play_alarm(r'D:\PROYECTOS_PY\deteccion_movimento_camara_seguridad\v1\development\sounds\sound_alarm_2.mp3')