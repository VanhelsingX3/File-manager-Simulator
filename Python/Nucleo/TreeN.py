from Nucleo.LinkedList import*
#from LinkedList import*
import sys
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import PyQt5.QtCore as core

class TreeN:
	def __init__(self):
		self.root = None									#Inicialmente no hay root.
		self.listToTextPlane = LinkedList()            		#LL Basica para simplemente guardar los nodos del arbol.					
		self.totalNodes = 0									#Un simple contador, para saber cuantos items hay en el arbol.
	
	#Agregar al arbol con sus respectivos parametros.
	def addElementoToTree(self,value,name,dad,typeDate):
		if(self.root == None and dad == 0):
			self.root = Node(value,name,typeDate,"/")
			#self.root.father = "/"
			self.final = None
			self.totalNodes += 1
			self.final2 = None
		else:
			self.addInner(value,name,dad,typeDate)

	#Agregado interno, haciendo uso de la funcion recursiva 'search'.	
	def addInner(self,value,name,dad,typeDate):
		current = self.searchInTree(dad)										#Busca y retorna el padre al que le sera agregado el elemento.
		if(self.root.children == None):											#Si no tiene hijos.
			self.root.children = LinkedList()
			self.root.tabulated = 0												#El root su tabulado es 0

		
		if(current != None):													#Si tiene hijos.
			if(current.children == None):
				current.children = LinkedList()
				newTab = 1 + current.tabulated
				current.children.add(value,name,typeDate,current,newTab)
				self.totalNodes += 1											#Contador.
				
			else:                
				newTab= 1 + current.tabulated
				current.children.add(value,name,typeDate,current,newTab)
				#current.children.searchInLL(value,0).father = current
				
				#nodeAdded = current.children.searchInLL(value,0)                
				
				#self.totalNodes += 1
		
		else:
			print('No se agrego al arbol')

	#Funcion que busca en el arbol.	
	def searchInTree(self,value):								
		return self.searchInnerInTree(self.root,value)				#Llama a la funcion interna.
	
	#Funcion recursiva interna de buscar dentro del arbol. Retornando en caso de una coincidencia.
	def searchInnerInTree(self,root,value):							
		if(self.root.value == value ):								#Si el item a buscar es el root
			return self.root										#Retorna el root

		if(root.children == None):									#Si el item no tiene hijos, caso que el dir no tenga elemento o el item sea un archivo.
			pass													#Salto.
		else:
			size = root.children.length()							#Guarda el tamano de la LL del hijo.
			for i in range(size):
				item = root.children.atPosition(i)					#Devuelve un elemento del ChildList y lo guarda en item.
				if(item.value == value):							#En caso de coincidencia.
					self.final = item								#Se agrega a la variable global final.					
				else:												#En caso no de haber coincidencia, hace el llamado recursivo con el nuevo elemento.
					self.searchInnerInTree(root.children.atPosition(i),value)	#Vuelve a llamarse.
		return self.final											#Devuelve el nodo encontrado. None, en caso que no.

	def searchInTreeForName(self,name):								
		return self.searchInnerInTreeForName(self.root,name)				#Llama a la funcion interna.
	
	#Funcion recursiva interna de buscar dentro del arbol. Retornando en caso de una coincidencia.
	def searchInnerInTreeForName(self,root,name):							
		if(self.root.name == name ):								#Si el item a buscar es el root
			return self.root										#Retorna el root

		if(root.children == None):									#Si el item no tiene hijos, caso que el dir no tenga elemento o el item sea un archivo.
			pass													#Salto.
		else:
			size = root.children.length()							#Guarda el tamano de la LL del hijo.
			for i in range(size):
				item = root.children.atPosition(i)					#Devuelve un elemento del ChildList y lo guarda en item.
				if(item.name == name):								#En caso de coincidencia.
					self.final2 = item								#Se agrega a la variable global final.					
				else:												#En caso no de haber coincidencia, hace el llamado recursivo con el nuevo elemento.
					self.searchInnerInTreeForName(root.children.atPosition(i),name)	#Vuelve a llamarse.
		return self.final2											#Devuelve el nodo encontrado. None, en caso que no.

	#Elimina un elemento en el arbol, incluyendo si este tiene hijos.	   
	def deleteElementToTree(self,element):							
		if(self.searchInTree(element) != None):
			temp = self.searchInTree(element).father              	#Guarda el nodo padre. 
			temp = temp.children
			temp.removeToNormal(element)
			print('Borrado')
		else:
			print('No pudo borrarse')

	#Este metodo guarda en una LL TODOS los nodos que existen en el arbol.
	def convertTreeToLL(self):										
		return self.convertInner(self.root)
	
	#Funcion recursiva para poder GUARDAR TODOS los nodos del arbol en una LL.
	def convertInner(self,root):										#Conversion a LL recursiva.
		if(root == self.root):
			self.listToTextPlane.add(self.root,None,None,None,None,False)				#Agregado al LL que sera usada para crear .mem

		if(root.children == None):
			pass
		else:
			size = root.children.length()
			for i in range(size):														#Recorrera los uhis 
				item = root.children.atPosition(i)
				self.listToTextPlane.add(item,None,None,None,None,False)
				self.convertInner(root.children.atPosition(i))							#Llamado recursivo.
		
	def addNewElements(self,NodeToAdd,fatherToAdd,objectToTree):						#[NodoPadre,Lista que se le extraera los elementos]
		if(NodeToAdd.children == None):
			pass
		else:
			size = NodeToAdd.children.length()
			for i in range(size):
				currentItem = NodeToAdd.children.atPosition(i)
				itemType = self.itemExtension(currentItem.name)
				if(currentItem.typeDate == 1):
					itemToAdd = QListWidgetItem(QIcon("Nucleo/Imagenes/folder.png"),currentItem.name)
					objectToTree.addElementoToTree(itemToAdd,currentItem.name,fatherToAdd,1)
				else:
					itemToAdd = QListWidgetItem(QIcon(itemType),currentItem.name)
					objectToTree.addElementoToTree(itemToAdd,currentItem.name,fatherToAdd,2)
				self.addNewElements(NodeToAdd.children.atPosition(i),itemToAdd,objectToTree)
	
	#Funcion para convertir el arbol en una Texto Plano y guardse en la carpeta /Memoria con el respectivo nombre del archivo.	
	def convertTreeToPlaneText(self,numberTree):
		self.convertTreeToLL()
		listTemp = self.listToTextPlane
		if(numberTree == 1):
			path = 'Memoria/Tree-A.mem'
		
		elif(numberTree == 2):
			path = 'Memoria/Tree-B.mem'

		self.clearContentOfPlaneText(numberTree)									#Limpia el contenido 'actual' del archivo.
	
		temp = open(path,"w") 														#Abre el texto plano.
		for i in range(listTemp.length()):											#Recorrera la lista que contiene todos los nodos del arbol.
			item = listTemp.atPosition(i)											#Extra un item de la LL
			temp.write("\t"*item.value.tabulated)									#Escribira el tabulado de dicho item.
			if(item.value.typeDate == 1):											#En caso que el nodo sea carpeta.
				temp.write("%s/" % (item.value.name))								#Escribira el nombre del nodo + /.
			else:																	#En caso que sea archivo.
				temp.write(item.value.name)
			temp.write('\n')														#Al final de cada linea salta de linea.
		temp.close()       
		self.listToTextPlane.first = None											#Se limpia la lista, SINO al siguiente guardado ira concatenando.
		

	#Extrae todos los elementos del texto plano, linea por linea.	
	def extracItemsToPlaneText(self,numberOfTree):
		lista = []
		self.listaFinal = []
		self.tabMax = 0
		tempParent = 0

		if(numberOfTree == 1):
			path = "Memoria/Tree-A.mem"
		if(numberOfTree == 2):
			path = "Memoria/Tree-B.mem"

		temp = open(path,"r")
		lineas = temp.readlines()
		for i in lineas:
			a = i.split("\t")
			lista.append(a)
		temp.close()

		#-------------------------------------------------------------
		#Quita el '\n' del final
		for k in range(len(lista)):
			for m in range(len(lista[k])):
				#lista[k][m] = lista[k][m].replace(" ","")
				lista[k][m] = lista[k][m].strip('\n')
		#-------------------------------------------------------------
		newList = []
		subList = []
		typeD = 1
		for n in range(len(lista)):
			tab = 0
			for i in range(len(lista[n])):
				currentIndex = lista[n][i]
				if(currentIndex == ''):
					tab += 1
				if(currentIndex != ''):
					if(currentIndex[-1] == '/'):
						typeD = 1
						currentIndex = currentIndex.strip('/')
					elif(currentIndex[-1] != '/'):
						typeD = 2
					subList.append(currentIndex)
					subList.append(typeD)
					subList.append(tab)
					newList.append(subList)
					subList = None
					subList = []
		return self.buildListToPlaneText(newList) 					#[value,typed,tabulated]

	#Asigna los respectivos padres a cada elemento, basado en su tabulado y recorrido de la lista dada.
	def buildListToPlaneText(self,_list):
		parentSaves = []
		parentSaves.append(_list[0][0])
		sizeOfList = len(_list)
		for i in range(1,sizeOfList):
			count = i + 1
			if(count < sizeOfList):
				if(_list[count][2] >= _list[i][2] or _list[i][2] == _list[i-1][2]):
					_list[i].append(parentSaves[-1])
					if(_list[i][2] != _list[count][2] and _list[i][2] < _list[count][2]):
						parentSaves.append(_list[i][0])
				if(_list[count][2] < _list[i][2]):
					tabu = _list[i][2] - _list[count][2]
					_list[i].append(parentSaves[-1])
					for j in range(0,tabu):
						parentSaves.pop()																	#-----
				count = 0
			else:
				_list[i].append(parentSaves[-1])
		return _list

	#Funcion para limpiar el contenido actual del archivo texto plano.
	def clearContentOfPlaneText(self,numberTree):	
		if(numberTree == 1):
			path = 'Memoria/Tree-A.mem'
		
		elif(numberTree == 2):
			path = 'Memoria/Tree-B.mem'
		
		f = open(path,"r") 
		lineas = f.readlines()
		f.close()
		f = open(path,"w")
		for linea in lineas:
			if linea==""+"\n":
				f.write(linea)
		f.close()
		
	#Esta funcion transforma una lista de elementos extraidos, agregandolos al arbol con sus respectivas transformaciones a items de tipo QListWidgetItem
	def convertPlaneTextToTree(self,numberOfTree):
		listItems = self.extracItemsToPlaneText(numberOfTree)			#[value,typeDate,tabulado,parent]
		listItems.pop(0)
		

		for i in range(len(listItems)):
			element = listItems[i]
			name = element[0]
			itemType = self.itemExtension(name)
			typedate = element[1]
			parent = self.searchInTreeForName(element[3]).value
			if(typedate == 1):
				value = QListWidgetItem(QIcon("Nucleo/Imagenes/folder.png"),name)
				self.addElementoToTree(value,name,parent,1)

			elif(typedate == 2):
				value = QListWidgetItem(QIcon(itemType),name)
				self.addElementoToTree(value,name,parent,2)
		

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