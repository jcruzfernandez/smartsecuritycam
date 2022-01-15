import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email():
	mensaje="""
	Posible alerta de robo verificar imagen adjunta de camara de seguridad\n 
	Mensaje enviado desde python
	"""
	asunto='Deteccion de movimiento!!'

	email=MIMEMultipart("alternative")
	email["Subject"]= asunto

	mensaje_text=MIMEText(mensaje)
	email.attach(mensaje_text)
	#adjuntado imagen
	ruta_imagen=r'captures_img/imagen_rec.jpg'
	imagen=open(ruta_imagen,"rb")
	contenido_adjunto=MIMEBase("aplication","octet-stream")
	contenido_adjunto.set_payload(imagen.read())
	encoders.encode_base64(contenido_adjunto)
	contenido_adjunto.add_header("Content-Disposition",
								f"attachment; filename={ruta_imagen}")
	email.attach(contenido_adjunto)
	mensaje_final=email.as_string()

	server=smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login('juliocruz552@gmail.com', 'razonamiento552')

	correos=("cristian1_552@hotmail.com",)
	for e in correos:
		server.sendmail('juliocruz552@gmail.com',
						'{}'.format(e), 
						mensaje_final)

	server.quit()
	print('Correo enviado exitosamente')
email()