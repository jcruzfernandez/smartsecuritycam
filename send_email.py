import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import imghdr
import argparse

parser=argparse.ArgumentParser(description='nombre de la imagen')
parser.add_argument('img')
args=parser.parse_args()

# Se plantea dos formas distintas en codigo para
# enviar correos de alerta con imgen adjunta

def email_1(img_name):
	mensaje="""
	\nPosible alerta de robo verificar\nimagen adjunta de camara de seguridad\n 
	Mensaje enviado desde python
	"""
	asunto='Deteccion de movimiento!!'

	email=MIMEMultipart("alternative")
	email["Subject"]= asunto

	mensaje_text=MIMEText(mensaje)
	email.attach(mensaje_text)
	#adjuntado imagen
	ruta_imagen=r'captures_img/{}.jpg'.format(str(img_name))
	imagen=open(ruta_imagen,"rb")
	contenido_adjunto=MIMEBase("aplication","octet-stream")
	contenido_adjunto.set_payload(imagen.read())
	encoders.encode_base64(contenido_adjunto)
	contenido_adjunto.add_header("Content-Disposition",
								f"attachment; filename={img_name}.jpg")
	email.attach(contenido_adjunto)
	mensaje_final=email.as_string()

	server=smtplib.SMTP('smtp.gmail.com',587) #465
	server.starttls()
	server.login('juliocruz552@gmail.com', 'razonamiento552')

	receptores=("cristian1_552@hotmail.com",)
	for receptor in receptores:
		server.sendmail('juliocruz552@gmail.com',
						'{}'.format(receptor), 
						mensaje_final)

	server.quit()
	print('Correo enviado exitosamente')

def email_2(img_name):

	mensaje = """
	Posible alerta de robo verificar,\nimagen adjunta de camara de seguridad\n
	Mensaje enviado desde python
	"""
	msg = EmailMessage()
	asunto ='Deteccion de movimiento!!'
	msg['Subject'] = asunto
	msg['From'] = 'juliocruz552@gmail.com'
	msg.set_content(mensaje)

	ruta_imagen = r'captures_img/{}.jpg'.format(str(img_name))
	imagen = open(ruta_imagen,"rb")
	file_data = imagen.read()
	file_type = imghdr.what(imagen.name)
	msg.add_attachment(file_data,maintype='image', subtype=file_type,
						filename=str(img_name))

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	#server.starttls()
	server.login('juliocruz552@gmail.com', 'razonamiento552')
	
	receptores = ("cristian1_552@hotmail.com",)

	for receptor in receptores:
		msg['To']= receptor
		server.send_message(msg)
	#server.quit()
	print('Correo enviado exitosamente')

# email_1(args.img)
email_2(args.img)