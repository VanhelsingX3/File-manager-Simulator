#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Nucleo.LinkedList import*
from Nucleo.TreeN import*
import sys
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import PyQt5.QtCore as core

class App(QMainWindow):

	FROM, SUBJECT, DATE = range(3)
	
	def __init__(self):
		super().__init__()
		self.title = 'SIMULADOR DE SISTEMA DE ARCHIVOS'
		self.setGeometry(0,0,800,350)									#[left,top,width,height]	
		QMainWindow.setWindowFlags(self, core.Qt.FramelessWindowHint)	#Quitar el borde por defecto de la ventana.
		self.setWindowIcon(QIcon("Nucleo/Imagenes/IconPrincipal.png"))
		
		paint = """
		QMainWindow{
	  	background-color: lightblue;
	  	color:black;
	  	background-image: url("Nucleo/Imagenes/barra.jpg");
	  	background-repeat:no-repeat;
		background-position:center top;
	
		}QPushButton{
			color:black;
			border-style: solid;
			border-radius: 7;
			padding: 5px;
			padding-left: 7px;
			padding-right: 30px;
			border-color: black;
			border-width: 2px;
			font-family:Georgia;
		}QListWidget{
			background-color: none;
		}QComboBox{
			background-color: lavender;
			color:black;
			border-radius: 7;
			padding: 5px;
			padding-left: 7px;
			padding-right: 30px;
			border-color: black;
			border-width: 2px;
			font-family:Georgia;
		}QToolButton{
			color:black;
			border-style: none;
			border-radius: 2;
			border-color: black;
			border-width: 1px;
			font-family:Georgia;
		}
		QMessageBox{
			background-color: lightGreen;
			color:red;
			font-family:Georgia;
		}
		QInputDialog{
			background-color:lightGreen;
			color:blue;
			
		}
		"""
		self.setStyleSheet(paint)										#Estableciendo el estilo de los Widgets

		#---------------------Creacion de objetos y variables.--------------------
		self.treeN1 = TreeN()											#Objeto donde tipo arbol para guardado de item del ListTree#1.
		self.treeN2 = TreeN()											#Objeto donde tipo arbol para guardado de item del ListTree#2.
		self.stateClickToList = None
		self.clickedItems1 = []								#LL para control/guardado de los elementos clickeados.
		self.clickedItems2 = []
		self.parent1 = None
		self.parent2 = None
		
		self.point1 = QListWidgetItem(QIcon("Nucleo/Imagenes/point.png"),"")
		self.pointPoint1 = QListWidgetItem(QIcon("Nucleo/Imagenes/pointPoint.png"),"")
		self.point2 = QListWidgetItem(QIcon("Nucleo/Imagenes/point.png"),"")
		self.pointPoint2 = QListWidgetItem(QIcon("Nucleo/Imagenes/pointPoint.png"),"")
		
		#-----------------Llamado de las funciones de ejecucion inicial.-----------------
		#NOTA: Los procedimientos para todo relacionado al arbol 2, se reutilizara codigo del arbol 1, por lo que este primero, su codigo no ira comentado.
		self.listWidget1()					
		self.listWidget2()
		self.addDirTree1("home",0)										#Agregado por defecto un root.					
		self.addDirTree2("home",0)										#Agregado por defecto un root.					

		self.clickedItems1.append(self.itemRoot1)																		
		self.clickedItems2.append(self.itemRoot2)																		
		self.buttonsTrees()
		self.otherButtons()
		self.littles()
		self.layoutTree()
		
		self.treeN1.convertPlaneTextToTree(1)
		self.treeN2.convertPlaneTextToTree(2)
		self.treeN1.convertTreeToPlaneText(1)
		self.treeN1.convertTreeToPlaneText(2)
		self.repaintListView(self.listTree1,self.itemRoot1,False)
		self.repaintListView(self.listTree2,self.itemRoot2,False)

		self.centerWindow()

	#Metodo de creacion/gestion de los botones de la ventana.	
	def buttonsTrees(self):
		#========================= Botones para tree #1 =========================
		self.btnTypeDate1 = QComboBox(self)									#Boton 'desplegable' para el tipo de dato.
		self.btnTypeDate1.addItem("Type Date")
		self.btnTypeDate1.addItem(QIcon("Nucleo/Imagenes/folder.png"),"Directory")
		self.btnTypeDate1.addItem(QIcon("Nucleo/Imagenes/file.png"),"File")
		self.btnTypeDate1.setToolTip('Seleccion del tipo de dato.')
		self.btnTypeDate1.currentIndexChanged.connect(self.enableBtnTypeData1)
		
		self.btnAdd1 = QPushButton(QIcon("Nucleo/Imagenes/add.png"),"Add")		#Boton de agregar
		self.btnAdd1.setIconSize(core.QSize(20,20))
		self.btnAdd1.setToolTip('Agregar elemento al arbol')				#Evento-mouse, se muestra un texto al pasar el puntero por el boton.
		self.btnAdd1.clicked.connect(self.enabledToClickAddButton1)			#Conexion de funcion al clickear al boton.
		
		self.btnDelete1 = QPushButton(QIcon("Nucleo/Imagenes/delete.png"),"Delete")
		self.btnDelete1.setIconSize(core.QSize(20,20))						#Define el tamano del icono.
		self.btnDelete1.setToolTip('Eliminar elemento del arbol')
		self.btnDelete1.clicked.connect(self.enabledToClikDeleteButton1)
		
		self.labelTextMessage1 = QLabel()
		self.labelTextMessage1.setEnabled(False)

		self.labelTextMessage2 = QLabel()
		self.labelTextMessage2.setEnabled(False)
		
		#========================= Botones para tree #2 =========================		
		self.btnTypeDate2 = QComboBox(self)
		self.btnTypeDate2.addItem("Type Date")
		self.btnTypeDate2.addItem(QIcon("Nucleo/Imagenes/folder.png"),"Directory")
		self.btnTypeDate2.addItem(QIcon("Nucleo/Imagenes/file.png"),"File")
		self.btnTypeDate2.setToolTip('Seleccion del tipo de dato.')
		self.btnTypeDate2.currentIndexChanged.connect(self.enableBtnTypeData2)

		self.btnAdd2 = QPushButton(QIcon("Nucleo/Imagenes/add.png"),"Add")
		self.btnAdd2.setIconSize(core.QSize(20,20))
		self.btnAdd2.setToolTip('Agregar elemento al arbol')
		self.btnAdd2.clicked.connect(self.enabledToClickAddButton2)

		self.btnDelete2 = QPushButton(QIcon("Nucleo/Imagenes/delete.png"),"Delete")
		self.btnDelete2.setIconSize(core.QSize(20,20))
		self.btnDelete2.setToolTip('Eliminar elemento del arbol')
		self.btnDelete2.clicked.connect(self.enabledToClikDeleteButton2)

	#Botones de control de la venta(cerrar, minimizar, expandir), derecha,izquierda
	def otherButtons(self):
		self.btnLeft = QPushButton(QIcon('Nucleo/Imagenes/left.png'),'')
		self.btnLeft.setToolTip('Trasladar item copiado a TreeList#1')
		self.btnLeft.clicked.connect(self.enableBtnLeft)
		
		self.btnRight = QPushButton(QIcon('Nucleo/Imagenes/right.png'),'')
		self.btnRight.setToolTip('Trasladar item copiado a TreeList#2')
		self.btnRight.clicked.connect(self.enableBtnRight)

		self.minimize = QToolButton(self)
		self.minimize.setIcon(QIcon("Nucleo/Imagenes/minimizeButton.png"))
		self.minimize.clicked.connect(self.minimizeWindow)
		self.minimize.setToolTip("Minimizar")

		self.maximize = QToolButton(self)
		self.maximize.setIcon(QIcon('Nucleo/Imagenes/maximizeButton.png'))
		self.maximize.clicked.connect(self.maximizeWindow)
		self.maximize.setToolTip("Maximizar")

		self.close = QToolButton(self)
		self.close.setIcon(QIcon('Nucleo/Imagenes/closeButton.png'))
		self.close.clicked.connect(self.closeWindow)
		self.close.setToolTip("Cerrar")

		self.minimize.setMinimumHeight(30)
		self.close.setMinimumHeight(50)
		self.maximize.setMinimumHeight(30)

		#Creacion de atajos de teclado para uso de las acciones en la interfaz.
		self.shortcutToAdd = QShortcut(QKeySequence("Ctrl+n"), self)             
		self.shortcutToAdd.activated.connect(self.enableEventToKeyboardToAdd)
		
		self.shortcutToDelete = QShortcut(QKeySequence("Del"), self)             
		self.shortcutToDelete.activated.connect(self.enableEventToKeyboardToDetele)
		
		self.shortcutToBack = QShortcut(QKeySequence("Backspace"), self)
		self.shortcutToBack.activated.connect(self.enableEventToKeyboardToBack)  

	def enableEventToKeyboardToAdd(self):
		if(self.stateClickToList == 1 ):
			self.enabledToClickAddButton1()
			
		elif(self.stateClickToList == 2):
			self.enabledToClickAddButton2()
		else:
			self.shortcutToAdd.setEnabled(False)

	def enableEventToKeyboardToDetele(self):
		if(self.stateClickToList == 1 ):
			self.enabledToClikDeleteButton1()
			
		elif(self.stateClickToList == 2):
			self.enabledToClikDeleteButton2()

		else:
			self.shortcutToDelete.setEnabled(False)

	def enableEventToKeyboardToBack(self):
		if(self.stateClickToList == 1 ):
			self.enableDoubleClickToPointPoint1()
			
		elif(self.stateClickToList == 2):
			self.enableDoubleClickToPointPoint2()

		else:
			self.shortcutToBack.setEnabled(False)

	#Establecimiento de los titulos de la segunda ventana.
	def littles(self):
		self.labelTitleWin2 = QLabel()
		self.labelTitleWin2.setStyleSheet('color: white')
		
		self.font = QFont()						#Personalizar los titulos
		self.font.setBold(True)
		self.font.setItalic(True)
		self.font.setWeight(True)
		self.font.setStyleStrategy(True)
		self.font.setStyleName('Arial')
		self.font.setStyleHint(True)
		self.font.setStyle(True)

		self.font2 = QFont()
		self.font2.setBold(True)
		self.font2.setUnderline(True)

		self.labelTitleWin2.setFont(self.font2)
		self.labelTitleWin2.setText("SELECT MULTIPLE APPLICATION")
		self.labelTitleWin2.setAlignment(core.Qt.AlignHCenter | core.Qt.AlignVCenter)		#Centrado del titulo.
		
		self.labelTitleTree1 = QLabel()
		self.labelTitleTree1.setFont(self.font)
		self.labelTitleTree1.setText("TREE LIST #1")
		self.labelTitleTree1.setAlignment(core.Qt.AlignHCenter | core.Qt.AlignVCenter)

		self.labelTitleTree2 = QLabel()
		self.labelTitleTree2.setFont(self.font)
		self.labelTitleTree2.setText("TREE LIST #2")
		self.labelTitleTree2.setAlignment(core.Qt.AlignHCenter | core.Qt.AlignVCenter)
		

	#Gestion y orden de los elementos en la ventana.
	def layoutTree(self):						
		self.hBtnLayout1 = QHBoxLayout()					#Orden horizontal(botones de control).
		self.hBtnLayout1.addWidget(self.btnTypeDate1)		
		self.hBtnLayout1.addWidget(self.btnAdd1)
		self.hBtnLayout1.addWidget(self.btnDelete1)

		self.vLayout1 = QVBoxLayout()						#Orden vertical
		self.vLayout1.addWidget(self.listTree1)				#2 La caja de visualizacion del arbol.
		self.vLayout1.addLayout(self.hBtnLayout1)			#3 Botones de control del treeList
		self.vLayout1.addWidget(self.labelTextMessage1)

		#Ordenamiento de los botones centrales.
		self.vTempLayout = QVBoxLayout()
		self.vTempLayout.addWidget(self.btnRight)
		self.vTempLayout.addWidget(self.btnLeft)

		self.vCentralLayout = QHBoxLayout()
		self.vCentralLayout.addLayout(self.vTempLayout)
		
		#Ordenamiento de lugares de los elementos graficos del tree#2
		self.hBtnLayout2 = QHBoxLayout()
		self.hBtnLayout2.addWidget(self.btnTypeDate2)
		self.hBtnLayout2.addWidget(self.btnAdd2)
		self.hBtnLayout2.addWidget(self.btnDelete2)

		self.vLayout2 = QVBoxLayout()
		self.vLayout2.addWidget(self.listTree2)				
		self.vLayout2.addLayout(self.hBtnLayout2)
		self.vLayout2.addWidget(self.labelTextMessage2)

		self.hPrincipalTitle = QHBoxLayout(self)
		self.hPrincipalTitle.addWidget(self.minimize)
		self.hPrincipalTitle.addWidget(self.maximize)
		self.hPrincipalTitle.addWidget(self.close)
		self.hPrincipalTitle.insertStretch(0)
		self.hPrincipalTitle.setSpacing(0)
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
		self.maxNormal = False									#Control de la venta de expandir.
		
		self.principalTitleLayout = QHBoxLayout(self)
		self.principalTitleLayout.addWidget(self.labelTitleWin2)
		self.principalTitleLayout.addLayout(self.hPrincipalTitle)
		self.principalTitleLayout.insertStretch(0)

		self.secondaryTitle = QHBoxLayout()
		self.secondaryTitle.addWidget(self.labelTitleTree1)
		self.secondaryTitle.addWidget(self.labelTitleTree2)

		self.semiFinalLayout = QHBoxLayout()					#Ordenamiento GENERAL(LA VENTANA) - Horizontal.
		self.semiFinalLayout.addLayout(self.vLayout1)			#Parte izquierda - Todo sobre el Arbol#1
		self.semiFinalLayout.addLayout(self.vCentralLayout)
		self.semiFinalLayout.addLayout(self.vLayout2)			#Parte derecha   -   Todo sobre el Arbol#2

		#Establece el orden final.
		self.vFinalLayout = QVBoxLayout()
		self.vFinalLayout.addLayout(self.principalTitleLayout)
		self.vFinalLayout.addLayout(self.secondaryTitle)
		self.vFinalLayout.addLayout(self.semiFinalLayout)
		
		self.ordenamiento = QWidget()
		self.ordenamiento.setLayout(self.vFinalLayout)
		self.setCentralWidget(self.ordenamiento)


	
	#-----------------------Funciones generales para establecer los arboles-------------------
	def listWidget1(self):												
		self.listTree1 = QListWidget()
		self.model = QAbstractItemView.ExtendedSelection								#Modo por defecto.
		self.listTree1.setSelectionMode(self.model)
		self.listTree1.setGeometry(QRect(10, 10, 211, 291))								#Dimensiones.
		self.listTree1.itemDoubleClicked.connect(self.enableDoubleClickItemTree1)		#Conexion al click doble de un item del TreeList#1
		self.listTree1.clicked.connect(self.enableClickInListWidget1)
		self.listTree1.itemSelectionChanged.connect(self.itemSelectionChanged1)

	def enableClickInListWidget1(self):
		self.stateClickToList = 1

	def itemSelectionChanged1(self):
		self.stateClickToList = 1

	def listWidget2(self):							
		self.listTree2 = QListWidget()
		self.listTree2.setSelectionMode(self.model)
		self.listTree2.setGeometry(QRect(10, 10, 211, 291))
		self.listTree2.itemDoubleClicked.connect(self.enableDoubleClickItemTree2)
		self.listTree2.activated.connect(self.enableClickInListWidget2)
		self.listTree2.itemSelectionChanged.connect(self.itemSelectionChanged2)

	def enableClickInListWidget2(self):
		self.stateClickToList = 2

	def itemSelectionChanged2(self):
		self.stateClickToList = 2

	#Metodo para agregar/convertir carpetas al TreeList#1 
	def addDirTree1(self,value,parent):									#[valor,padre]				
		if(isinstance(value,str) == True):
			item = QListWidgetItem(QIcon("Nucleo/Imagenes/folder.png"),value)
			self.treeN1.addElementoToTree(item,value,parent,1)	
			if(parent == 0):
				self.itemRoot1 = self.treeN1.searchInTree(item) 	
		else:
			self.listTree1.addItem(value)
			name = value.text()	
			self.treeN1.addElementoToTree(value,name,parent,1)
			
	def addDirTree2(self,value,parent):
		if(isinstance(value,str) == True):
			item = QListWidgetItem(QIcon("Nucleo/Imagenes/folder.png"),value)
			self.treeN2.addElementoToTree(item,value,parent,1)
			if(parent == 0):
				self.itemRoot2 = self.treeN2.searchInTree(item)
		else:
			self.listTree2.addItem(value)
			name = value.text()	
			self.treeN2.addElementoToTree(value,name,parent,1)
		
	#Metodo para agregar/convertir archivos al TreeList#1
	def addFileTree1(self,value,parent):
		itemType = self.itemExtension(value)
		item = QListWidgetItem(QIcon(itemType),value)
		if(parent == 0):												
			self.itemRoot1 = item
		self.treeN1.addElementoToTree(item,value,parent,2)				#[valor,nombre,padre,tyDate]; typeDate == 2 para archivo.
		
	def addFileTree2(self,value,parent):
		itemType = self.itemExtension(value)
		item = QListWidgetItem(QIcon(itemType),value)
		if(parent == 0):												
			self.itemRoot2 = item
		self.treeN2.addElementoToTree(item,value,parent,2)

	#Define un tipo de icono dependiendo de la extension del archivo.
	def itemExtension(self,item):
		ext = item.split(".")
		if(len(ext)!= 1):
			if(ext[1]=="txt"):
				return "Nucleo/Imagenes/file.png"
			elif(ext[1]=="mp3"):
				return "Nucleo/Imagenes/Mp3.png"
			elif(ext[1]=="pdf"):
				return	"Nucleo/Imagenes/pdf.png"
			elif(ext[1]=="py"):
				return	"Nucleo/Imagenes/py.png"
			elif(ext[1]=="js"):
				return "Nucleo/Imagenes/js.png"
			elif(ext[1]=="html"):
				return "Nucleo/Imagenes/html.png"
		else:
			return "Nucleo/Imagenes/file.png"
		
		return "Nucleo/Imagenes/file.png"


#=============== METODOS QUE DEFINEN/ACIONAN/ACTIVA EN DETERMINADOS EVENTOS SOBRE LAS HERRAMIENTAS(BOTONES,CAJAS ETC.)==================	
	#----------------------ARBOL #1----------------------
	#Metodo que ejecuta al presionar en agregar, tambien gestiona el agregado, si hay items repetidos, este niegua el agregado y manda un mensaje.
	def enabledToClickAddButton1(self):
		self.btnTypeDate1.setEnabled(True)
		self.enableLabels1(False)
		currentFatherToList = self.treeN1.searchInTree(self.clickedItems1[-1].value)										#Nodo padre de la lista actual.

		self.dlg1 =  QInputDialog(self,Qt.WindowSystemMenuHint | Qt.WindowTitleHint | core.Qt.FramelessWindowHint)
		self.dlg1.setLabelText("Ingrese el valor a agregar a la lista #1.")
		okPressed = self.dlg1.exec_()
		valueToAdd = self.dlg1.textValue()                                          
		self.dlg1.resize(300,100) 

		if(okPressed == True and valueToAdd != ''):	
			if(self.btnTypeDate1.currentIndex() == 1):
				self.enableLabels1(False)
				if(currentFatherToList.children != None):
					if(currentFatherToList.children.searchItemForNameAndType(valueToAdd,1) != True):		#Aqui verifica si hay un nodo con el mismo nombre y tipo.
						self.addDirTree1(valueToAdd,currentFatherToList.value)											#En caso que no existe el mismo, se agrega.
					else:
						self.enableLabels1(True,"Ya existe un elemento con ese nombre.")
				else:					
					self.addDirTree1(valueToAdd,currentFatherToList.value)

			elif(self.btnTypeDate1.currentIndex() == 2):
				self.enableLabels1(False)
				if(currentFatherToList.children != None):
					if(currentFatherToList.children.searchItemForNameAndType(valueToAdd,2) != True):
						self.addFileTree1(valueToAdd,currentFatherToList.value)
					else:
						self.enableLabels1(True,"Ya existe un elemento con ese nombre.")
				else:
					self.addFileTree1(valueToAdd,currentFatherToList.value)			
			else:
				self.labelTextMessage1.setEnabled(True)
				self.enableLabels1(True,'¡Elija el tipo de dato!')
		
		if(currentFatherToList.name != 'home'):
			self.repaintListView(self.listTree1,currentFatherToList)
		elif(currentFatherToList.name == 'home'):
			self.repaintListView(self.listTree1,currentFatherToList,False)	
		self.treeN1.convertTreeToPlaneText(1)		                 

	def enabledToClikDeleteButton1(self):
		listSelected = self.listTree1.selectedItems()
		if(len(listSelected) != 0):  	
			self.enableLabels1(False)		
			itemFather = self.treeN1.searchInTree(listSelected[0]).father
			for i in range(len(listSelected)):
				self.treeN1.deleteElementToTree(listSelected[i])
			if(itemFather.name != 'home'):
				self.repaintListView(self.listTree1,itemFather)
			elif(itemFather.name == 'home'):
				self.repaintListView(self.listTree1,itemFather,False)
		else:
			self.enableLabels1(True,'¡Seleccione elementos para borrar!')	
		self.treeN1.convertTreeToPlaneText(1)

	#Metodo que conecta al clickear 2 veces en un item del TreeList
	def enableDoubleClickItemTree1(self):
		self.enableLabels1(False)			
		self.btnTypeDate1.setEnabled(True)
		self.parent1 = self.listTree1.currentItem()				#Retorna el item clickeado 2 veces en el TreeList.
		clickedFather = self.treeN1.searchInTree(self.parent1)
		
		if(self.parent1 == self.pointPoint1):					#En caso de presionar el ".."
			self.enableDoubleClickToPointPoint1()

		if(self.parent1 == self.point1):
			print("Actualmente esta en el directorio '%s'" % self.clickedItems1[-1].name)
			
		elif(self.parent1 != self.point1 and self.parent1 != self.pointPoint1):
			intTypeDate = self.treeN1.searchInTree(self.parent1).typeDate
			self.clickedItems1.append(clickedFather)

			if(intTypeDate == 1):
				self.stateToElementsTree1(True)
				if(self.parent1.text() == "Root"):
					pass
				
				temp = self.treeN1.searchInTree(self.parent1)					#Busca y devuelve el Nodo en el arbol.
				self.repaintListView(self.listTree1,temp)

			else:
				self.enableLabels1(True,'¡No es un directorio!')

	def enableDoubleClickToPointPoint1(self):
		self.enableLabels1(False)
		if(len(self.clickedItems1) > 1):				
			tempParentClick = self.treeN1.searchInTree(self.clickedItems1[-1].value)		#Devuelve el NODO padre anterior.
			if(isinstance(tempParentClick.father,str) != True):
				if(self.clickedItems1[-2].name == 'home'):
					self.repaintListView(self.listTree1,tempParentClick.father,False)
					self.clickedItems1.pop()	
				else:
					self.repaintListView(self.listTree1,tempParentClick.father)
					self.clickedItems1.pop()
			else:
				if(self.clickedItems1[-2].name == 'home'):
					self.repaintListView(self.listTree1,tempParentClick.father,False)
					self.clickedItems1.pop()
				else:
					self.cleanListView(self.listTree1)
					self.listTree1.addItem(self.itemRoot1.value)
					self.stateToElementsTree1(False)

	#ACTIVACION GENERAL DE HERRAMIENTAS.
	def stateToElementsTree1(self,state):
		self.btnAdd1.setEnabled(state)
		self.btnDelete1.setEnabled(state)
		self.labelTextMessage1.setEnabled(state)
		self.btnRight.setEnabled(state)
		self.btnTypeDate1.setEnabled(state)
		self.shortcutToAdd.setEnabled(state)
		self.shortcutToDelete.setEnabled(state)

	def enableBtnTypeData1(self):
		self.enableLabels1(False)
		if(self.btnTypeDate1.currentIndex() == 0):
			self.enableLabels1(True,'¡Elija el tipo de dato!')
		else:
			self.labelTextMessage1.setVisible(False)

	def enableLabels1(self,state,text = ''):
		self.labelTextMessage1.setVisible(state)
		self.labelTextMessage1.setEnabled(state)
		self.labelTextMessage1.setText(text)
		self.labelTextMessage1.setStyleSheet('QLabel {color: red}')
		self.labelTextMessage1.setFont(QFont("Times Font", 12))
	
	#----------------------- A R B O L #2-------------------------
	def enabledToClickAddButton2(self):
		self.btnTypeDate2.setEnabled(True)
		self.enableLabels2(False)
		currentFatherToList = self.treeN2.searchInTree(self.clickedItems2[-1].value)										#Nodo padre de la lista actual.

		self.dlg2 =  QInputDialog(self,Qt.WindowSystemMenuHint | Qt.WindowTitleHint | core.Qt.FramelessWindowHint)
		self.dlg2.setLabelText("Ingrese el valor a agregar a la lista #2.")
		okPressed = self.dlg2.exec_()
		valueToAdd = self.dlg2.textValue()                                          
		self.dlg2.resize(300,100) 

		if(okPressed == True and valueToAdd != ''):	
			if(self.btnTypeDate2.currentIndex() == 1):
				self.enableLabels2(False)
				if(currentFatherToList.children != None):
					if(currentFatherToList.children.searchItemForNameAndType(valueToAdd,1) != True):		#Aqui verifica si hay un nodo con el mismo nombre y tipo.
						self.addDirTree2(valueToAdd,currentFatherToList.value)											#En caso que no existe el mismo, se agrega.
					else:
						self.enableLabels2(True,"Ya existe un elemento con ese nombre.")
				else:
					self.addDirTree2(valueToAdd,currentFatherToList.value)
					
			elif(self.btnTypeDate2.currentIndex() == 2):
				self.enableLabels2(False)
				if(currentFatherToList.children != None):
					if(currentFatherToList.children.searchItemForNameAndType(valueToAdd,2) != True):
						self.addFileTree2(valueToAdd,currentFatherToList.value)
					else:
						self.enableLabels2(True,"Ya existe un elemento con ese nombre.")
				else:
					self.addFileTree2(valueToAdd,currentFatherToList.value)			
			else:
				self.labelTextMessage2.setEnabled(True)
				self.enableLabels2(True,'¡Elija el tipo de dato!')
		
		if(currentFatherToList.name != 'home'):
			self.repaintListView(self.listTree2,currentFatherToList)
		elif(currentFatherToList.name == 'home'):
			self.repaintListView(self.listTree2,currentFatherToList,False)	
		self.treeN2.convertTreeToPlaneText(2)

	def enabledToClikDeleteButton2(self):
		listSelected = self.listTree2.selectedItems()
		if(len(listSelected) != 0):  	
			self.enableLabels2(False)
			itemFather = self.treeN2.searchInTree(listSelected[0]).father
			for i in range(len(listSelected)):
				self.treeN2.deleteElementToTree(listSelected[i])
			if(itemFather.name != 'home'):
				self.repaintListView(self.listTree2,itemFather)
			elif(itemFather.name == 'home'):
				self.repaintListView(self.listTree2,itemFather,False)			
		else:
			self.enableLabels2(True,'¡Seleccione elementos para borrar!')
		self.treeN2.convertTreeToPlaneText(2)

	#Metodo que conecta al clickear 2 veces en un item del TreeList
	def enableDoubleClickItemTree2(self):
		self.enableLabels2(False)
		self.btnTypeDate2.setEnabled(True)			
		self.parent2 = self.listTree2.currentItem()				#Retorna el item clickeado 2 veces en el TreeList.
		clickedFather = self.treeN2.searchInTree(self.parent2)
		
		if(self.parent2 == self.pointPoint2):					#En caso de presionar el ".."
			self.enableDoubleClickToPointPoint2()			

		if(self.parent2 == self.point2):
			print("Actualmente esta en el directorio '%s" % self.clickedItems2[-1].name)
			
		elif(self.parent2 != self.point2 and self.parent2 != self.pointPoint2):
			intTypeDate = self.treeN2.searchInTree(self.parent2).typeDate
			self.clickedItems2.append(clickedFather)
			if(intTypeDate == 1):
				self.stateToElementsTree2(True)
				if(self.parent2.text() == "Root"):
					pass
				temp = self.treeN2.searchInTree(self.parent2)					#Busca y devuelve el Nodo en el arbol.
				self.repaintListView(self.listTree2,temp)
			else:
				self.enableLabels2(True,'¡No es un directorio!')
		if(len(self.clickedItems2)>0):
			pass

	def enableDoubleClickToPointPoint2(self):
		self.enableLabels2(False)	
		if(len(self.clickedItems2) > 1):				
			tempParentClick = self.treeN2.searchInTree(self.clickedItems2[-1].value)		#Devuelve el NODO padre anterior.
			if(isinstance(tempParentClick.father,str) != True):
				if(self.clickedItems2[-2].name == 'home'):
					self.repaintListView(self.listTree2,tempParentClick.father,False)
					self.clickedItems2.pop()	
				else:
					self.repaintListView(self.listTree2,tempParentClick.father)
					self.clickedItems2.pop()
			else:
				if(self.clickedItems2[-2].name == 'home'):
					self.repaintListView(self.listTree2,tempParentClick.father,False)
					self.clickedItems2.pop()
				else:		
					self.cleanListView(self.listTree2)
					self.listTree2.addItem(self.itemRoot2.value)
					self.stateToElementsTree2(False)
		
	def enableBtnTypeData2(self):
		self.enableLabels2(False)
		if(self.btnTypeDate2.currentIndex() == 0):
			self.enableLabels2(True,'¡Elija el tipo de dato!')
		else:
			self.labelTextMessage2.setVisible(False)
	
	def stateToElementsTree2(self,state):
		self.btnAdd2.setEnabled(state)
		self.btnDelete2.setEnabled(state)
		self.labelTextMessage2.setEnabled(state)
		self.btnLeft.setEnabled(state)
		self.btnTypeDate2.setEnabled(state)
		self.shortcutToAdd.setEnabled(state)
		self.shortcutToDelete.setEnabled(state)

	def enableLabels2(self,state,text = ''):
		self.labelTextMessage2.setVisible(state)
		self.labelTextMessage2.setEnabled(state)
		self.labelTextMessage2.setText(text)
		self.labelTextMessage2.setStyleSheet('QLabel {color: red}')
		self.labelTextMessage2.setFont(QFont("Times Font", 12))


	#============================== General ============================
	#Metodo para limpiar el TreeList, recibiendo como parametro, al TreeList"[1 or 2]".
	def cleanListView(self,listObject):	
		sizeToList = listObject.count()
		for i in range(0,sizeToList):
			size = listObject.count()
			while(size !=0):
				listObject.takeItem(i)
				size = listObject.count()
			listObject.update()		
		listObject.repaint()

	#Funcion para repintar el ListView	
	def repaintListView(self,listObject,item,statePoint = True):				#[Arbol a pintar,desde que item pintar]													#<=======
		self.cleanListView(listObject)
		if(statePoint == True):
			if(listObject == self.listTree1):
				listObject.addItem(self.point1)
				listObject.addItem(self.pointPoint1)
			if(listObject == self.listTree2):
				listObject.addItem(self.point2)
				listObject.addItem(self.pointPoint2)

		if(item.children != None):
			item.children.sortLL()
			size = item.children.length()
			for i in range(0,size):
				tempo = item.children.atPosition(i).value
				listObject.addItem(tempo)
		
	#Funcion al boton de flecha derecha, lo cual pega al TreeList#2 los elementos seleccionados.
	def enableBtnRight(self):
		self.enableLabels1(False)
		listSelected = self.listTree1.selectedItems()															#Guarda los items seleccionados.
		listTemp = LinkedList()
		currentFather = self.treeN2.searchInTree(self.clickedItems2[-1].value)									#Retorna el elemento al que se le pegara los items.
		if(len(listSelected) != 0):																				#En caso que haya seleccionado.															
			for i in range(len(listSelected)):
				currentCopied = self.treeN1.searchInTree(listSelected[i])
				if(currentCopied.typeDate == 1):																#En caso que sea carpeta.
					itemToAdd = QListWidgetItem(QIcon("Nucleo/Imagenes/folder.png"),currentCopied.name)
					if(currentFather.children != None):
						if(currentFather.children.searchItemForNameAndType(currentCopied.name,1) == True):
							currentFather.children.removeForNameAndType(currentCopied.name,1)		
							self.warningMessage("Elemento ya existente","El elemento '%s' ha sido reemplazado"%(currentCopied.name))
							self.addDirTree2(itemToAdd,currentFather.value)
						else:
							self.addDirTree2(itemToAdd,currentFather.value)
					else:
						self.addDirTree2(itemToAdd,currentFather.value)
					newFather = self.treeN2.searchInTree(itemToAdd)
					self.treeN2.addNewElements(currentCopied,newFather.value,self.treeN2)
				elif(currentCopied.typeDate == 2):																#En caso que sea archivo.
					if(currentFather.children != None):
						if(currentFather.children.searchItemForNameAndType(currentCopied.name,2) == True):
							currentFather.children.removeForNameAndType(currentCopied.name,2)
							self.warningMessage("Elemento ya existente","El elemento '%s' ha sido reemplazado"%(currentCopied.name))	
							self.addFileTree2(currentCopied.name,currentFather.value)
						else:
							self.addFileTree2(currentCopied.name,currentFather.value)
					else:
						self.addFileTree2(currentCopied.name,currentFather.value)
			if(currentFather.name != 'home'):
				self.repaintListView(self.listTree2,currentFather)
			elif(currentFather.name == 'home'):
				self.repaintListView(self.listTree2,currentFather,False)	
			self.treeN2.convertTreeToPlaneText(2)			
		else:
			self.enableLabels1(True,'¡No hay elementos copiados!')		
	
	#Funcionamiento para el boton flecha izqueirda utilizado para pegar los elementos copiados.
	def enableBtnLeft(self):
		self.enableLabels2(False)
		listSelected = self.listTree2.selectedItems()															#Guarda los items seleccionados.
		listTemp = LinkedList()
		currentFather = self.treeN1.searchInTree(self.clickedItems1[-1].value)									#Retorna el elemento al que se le pegara los items.
		if(len(listSelected) != 0):																				#En caso que haya seleccionado.															
			for i in range(len(listSelected)):
				currentCopied = self.treeN2.searchInTree(listSelected[i])
				if(currentCopied.typeDate == 1):																					
					itemToAdd = QListWidgetItem(QIcon("Nucleo/Imagenes/folder.png"),currentCopied.name)
					if(currentFather.children != None):
						if(currentFather.children.searchItemForNameAndType(currentCopied.name,1) == True):
							currentFather.children.removeForNameAndType(currentCopied.name,1)		
							self.warningMessage("Elemento ya existente","El elemento '%s' ha sido reemplazado"%(currentCopied.name))
							self.addDirTree1(itemToAdd,currentFather.value)
						else:
							self.addDirTree1(itemToAdd,currentFather.value)
					else:
						self.addDirTree1(itemToAdd,currentFather.value)
					newFather = self.treeN1.searchInTree(itemToAdd)
					self.treeN1.addNewElements(currentCopied,newFather.value,self.treeN1)
				elif(currentCopied.typeDate == 2):
					if(currentFather.children != None):
						if(currentFather.children.searchItemForNameAndType(currentCopied.name,2) == True):
							currentFather.children.removeForNameAndType(currentCopied.name,2)
							self.warningMessage("Elemento ya existente","El elemento '%s' ha sido reemplazado"%(currentCopied.name))	
							self.addFileTree1(currentCopied.name,currentFather.value)
						else:
							self.addFileTree1(currentCopied.name,currentFather.value)
					else:
						self.addFileTree1(currentCopied.name,currentFather.value)
			if(currentFather.name != 'home'):
				self.repaintListView(self.listTree1,currentFather)
			elif(currentFather.name == 'home'):
				self.repaintListView(self.listTree1,currentFather,False)	
			self.treeN1.convertTreeToPlaneText(1)			
		else:
			self.enableLabels2(True,'¡No hay elementos copiados!')		

	#Centrado de la ventana.		
	def centerWindow(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move(size.width()/2,size.height()/2)

	#Funcjon al boton minimizar ventana.
	def minimizeWindow(self):
		self.showMinimized()

	#Funcion al boton cerrar ventana.
	def closeWindow(self):
		sys.exit()
	
	#Funcion al boton maximizar ventana.
	def maximizeWindow(self):
		if(self.maxNormal):
			self.showNormal()
			self.maxNormal= False
		else:
			self.showMaximized()
			self.maxNormal=  True

	#Envia un mensaje de alerta.
	def warningMessage(self, Title, message): 
		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Warning)
		self.msg.setText(message)
		self.msg.setWindowTitle(Title)
		self.btnOk = QPushButton("Aceptar")
		self.msg.addButton(self.btnOk,QMessageBox.YesRole)           
		self.msg.show()
		self.msg.exec_()
	

			
