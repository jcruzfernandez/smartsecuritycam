from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

bgFondo1="#0a0a0a"
bgBLue= "#186cf7"


def only_numeric(P):
    #Verifica si el valor ingresado en los ENTRY son numericos o vacios y retorna un boleano
    if P == "" or len(P)<=9 and P.isdigit():
        return True
    return False

def connectDB():
	conn=sqlite3.connect("db_whatsapp.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS dbwhatsapp (id INTEGER PRIMARY KEY, Nombre text, Numero text)")
	conn.commit()
	conn.close()

def insertDB(nombre, numero):
	conn=sqlite3.connect("db_whatsapp.db")
	cur=conn.cursor()
	cur.execute("INSERT INTO dbwhatsapp VALUES (NULL,?,?)",(nombre, numero))
	conn.commit()
	conn.close()

def viewAllDB():
	conn=sqlite3.connect("db_whatsapp.db")
	cur=conn.cursor()
	cur.execute("SELECT * FROM dbwhatsapp")
	rows=cur.fetchall()
	conn.close()
	return rows

def deleteAllDB():
	conn=sqlite3.connect("db_whatsapp.db")
	cur=conn.cursor()
	cur.execute("DELETE FROM dbwhatsapp")
	conn.commit()
	conn.close()

def deleteSelectDB(id):
	conn=sqlite3.connect("db_whatsapp.db")
	cur=conn.cursor()
	cur.execute("DELETE FROM dbwhatsapp WHERE id=?",(id,))
	conn.commit()
	conn.close()

def add_record():
	global e_numero, e_nombre
	if e_nombre.get()!= "" or e_numero.get()!="":
		if e_numero.get().isdigit():
			insertDB(e_nombre.get(),e_numero.get())
			viewAll_records()
			e_nombre.set("")
			e_numero.set("")
		else:
			messagebox.showwarning('Alerta', 'Escriba un numero valido')
	else:
		messagebox.showwarning('Alerta', 'Ingrese datos antes de agregar')
def viewAll_records():
	global tv, e_numero, e_nombre
	records=tv.get_children()
	for i in records:
		tv.delete(i)
	cur=viewAllDB()
	for (ID, name, numero) in cur:
		tv.insert('',0,text=ID,values=(name, numero))

def deleteSelect_record():
	if messagebox.askyesno(message="¿Desea borrar el numero?",
							title="Borrar numero seleccionado")==True:
		r=tv.item(tv.selection())["text"]
		deleteSelectDB(r)
		viewAll_records()
def deleteAll_records():
	if messagebox.askyesno(message="¿Desea borrar todos los numeros?",
							title="Borrar todo registro")==True:
		deleteAllDB()
		viewAll_records()

def toplevel_whatsapp():
	connectDB()
	global tv, e_nombre, e_numero
	ventanaDB=Toplevel()#Tk()
	ventanaDB.title('Numeros de WhatsApp asociados')
	ventanaDB.geometry('472x405')
	ventanaDB.iconbitmap(r"D:\PROYECTOS_PY\deteccion_movimento_camara_seguridad\v1\development\icons\whatsapp_chat2.ico")
	# Creacion de Widgets
	# Etiquetas
	label_nombre = Label(ventanaDB,text="Nombre",fg="#186cf7", font= ('Helvetica', 10, 'bold'),bg=bgFondo1)
	label_correo = Label(ventanaDB,text="Numero",fg="#186cf7", font= ('Helvetica', 10, 'bold'),bg=bgFondo1)
	label_nombre.grid(column=1, row=1, columnspan = 2)
	label_correo.grid(column=1, row=2, columnspan = 2)
	# Entrys
	e_nombre = StringVar(ventanaDB)
	e_numero = StringVar(ventanaDB)
	callback=ventanaDB.register(only_numeric)
	Entry_nombre = Entry(ventanaDB, textvariable=e_nombre, width=35, justify='left')#, validate="key")
	Entry_numero = Entry(ventanaDB, textvariable=e_numero, width=35, justify='left',
						validate="key", validatecommand=(callback, '%P'))#, validate="key")
	Entry_nombre.grid(column=3, row=1, padx=5, pady=5, columnspan = 3)
	Entry_numero.grid(column=3, row=2, padx=5, pady=5, columnspan = 3)
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
	tv.heading("col2", text= "Numero", anchor=CENTER)

	tv.tag_configure('oddrow', background='white')
	tv.tag_configure('evenrow', background='lightblue')

	tv.grid(column=1, row=4, padx=5, pady=5, columnspan = 6)

	ventanaDB.configure(background=bgFondo1)
	ventanaDB.resizable(0, 0)
	ventanaDB.mainloop()