from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

bgFondo1="#0a0a0a"
bgBLue= "#186cf7"

def connectDB():
	conn=sqlite3.connect("db_email.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS dbemail (id INTEGER PRIMARY KEY, Nombre text, Correo text)")
	conn.commit()
	conn.close()

def insertDB(nombre, correo):
	conn=sqlite3.connect("db_email.db")
	cur=conn.cursor()
	cur.execute("INSERT INTO dbemail VALUES (NULL,?,?)",(nombre, correo))
	conn.commit()
	conn.close()

def viewAllDB():
	conn=sqlite3.connect("db_email.db")
	cur=conn.cursor()
	cur.execute("SELECT * FROM dbemail")
	rows=cur.fetchall()
	conn.close()
	return rows

def deleteAllDB():
	conn=sqlite3.connect("db_email.db")
	cur=conn.cursor()
	cur.execute("DELETE FROM dbemail")
	conn.commit()
	conn.close()

def deleteSelectDB(id):
	conn=sqlite3.connect("db_email.db")
	cur=conn.cursor()
	cur.execute("DELETE FROM dbemail WHERE id=?",(id,))
	conn.commit()
	conn.close()

def add_record():
	global e_correo, e_nombre
	if e_nombre.get()!= "" or e_correo.get()!="":
		if "@" in e_correo.get():
			insertDB(e_nombre.get(),e_correo.get())
			viewAll_records()
			e_nombre.set("")
			e_correo.set("")
		else:
			messagebox.showwarning('Alerta', 'Escriba un correo valido')
	else:
		messagebox.showwarning('Alerta', 'Ingrese datos antes de agregar')
def viewAll_records():
	global tv, e_correo, e_nombre
	records=tv.get_children()
	for i in records:
		tv.delete(i)
	cur=viewAllDB()
	for (ID, name, correo) in cur:
		tv.insert('',0,text=ID,values=(name, correo))

def deleteSelect_record():
	if messagebox.askyesno(message="¿Desea borrar el correo?",
							title="Borrar correo seleccionado")==True:
		r=tv.item(tv.selection())["text"]
		deleteSelectDB(r)
		viewAll_records()
def deleteAll_records():
	if messagebox.askyesno(message="¿Desea borrar todos los correos?",
							title="Borrar todo registro")==True:
		deleteAllDB()
		viewAll_records()

def toplevel_email():
	connectDB()
	global tv, e_correo, e_nombre
	ventanaDB=Toplevel()#Tk()
	ventanaDB.title('Correos asociados')
	ventanaDB.geometry('472x405')
	ventanaDB.iconbitmap(r"D:\PROYECTOS_PY\deteccion_movimento_camara_seguridad\v1\development\icons\email_send2.ico")
	# Creacion de Widgets
	# Etiquetas
	label_nombre = Label(ventanaDB,text="Nombre",fg="#186cf7", font= ('Helvetica', 10, 'bold'),bg=bgFondo1)
	label_correo = Label(ventanaDB,text="Correo",fg="#186cf7", font= ('Helvetica', 10, 'bold'),bg=bgFondo1)
	label_nombre.grid(column=1, row=1, columnspan = 2)
	label_correo.grid(column=1, row=2, columnspan = 2)
	# Entrys
	e_nombre = StringVar(ventanaDB)
	e_correo = StringVar(ventanaDB)
	Entry_nombre = Entry(ventanaDB, textvariable=e_nombre, width=35, justify='left')#, validate="key")
	Entry_correo = Entry(ventanaDB, textvariable=e_correo, width=35, justify='left')#, validate="key")
	Entry_nombre.grid(column=3, row=1, padx=5, pady=5, columnspan = 3)
	Entry_correo.grid(column=3, row=2, padx=5, pady=5, columnspan = 3)
	# Botones
	btnAdd = Button(ventanaDB,text="Agregar",width=20, command=add_record)
	btnViewAll = Button(ventanaDB,text="Ver todo",width=20, command=viewAll_records)
	btnDeleteSelect = Button(ventanaDB, text="Eliminar selección", width=20, command=deleteSelect_record)
	btnDeleteAll = Button(ventanaDB, text="Eliminar todo", width=20, command=deleteAll_records)
	btnAdd.grid(column=1, row=3, padx=5, pady=5, columnspan = 2)
	btnViewAll.grid(column=5, row=3, padx=5, pady=5, columnspan = 2)
	btnDeleteSelect.grid(column=1, row=6, padx=5, pady=5,columnspan = 2)
	btnDeleteAll.grid(column=5, row=6, padx=5, pady=5,columnspan = 2)

	#Estilo de la tabla TreeView
	style=ttk.Style()
	style.theme_use("alt")
	tv=ttk.Treeview(ventanaDB,columns=("col1","col2"))
	tv.column("#0",anchor= W, width=50)
	tv.column("col1",anchor= W, width=150)
	tv.column("col2",anchor= W, width=255)

	tv.heading("#0", text= "Item", anchor=CENTER)
	tv.heading("col1", text= "Nombre", anchor=CENTER)
	tv.heading("col2", text= "Email", anchor=CENTER)

	tv.tag_configure('oddrow', background='white')
	tv.tag_configure('evenrow', background='lightblue')

	tv.grid(column=1, row=4, padx=5, pady=5, columnspan = 6)

	ventanaDB.configure(background=bgFondo1)
	ventanaDB.resizable(0, 0)
	ventanaDB.mainloop()