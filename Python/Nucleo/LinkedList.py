from Nucleo.Compare import*
#from Compare import*

class Node:
	def __init__(self,value,name,typeDate,father = None,tabulated = 1):
		self.value = value
		self.name = name
		self.next = None
		self.children = None
		self.father = father
		self.typeDate = typeDate
		self.tabulated = tabulated

class LinkedList:
	def __init__(self):
		self.first = None
		self.listType2 = []
		
	def add(self,value,name,typeDate,father,tabulated,state = True):								#Agregar elemento
		if(state == True):	
			if(not self.first):
				self.first = Node(value,name,typeDate,father,tabulated)
			
			else:
				compare = Compare() #Crea una instancia de la clase
				if(compare.compare(self.first.name,name) > 0):
					stack = self.first
					self.first = Node(value,name,typeDate,father,tabulated)
					self.first.next = stack	

					return True
				else:
					previous = self.first
					current = self.first.next
					
					while(current):
						#Cuando el valor del actual sea < que value, devuelve -1
						#cuando el valor del current sea = a value, devuelve 0
						#cuando el valor del current sea > a value, devuelve 1
						if(compare.compare(current.name,name)<0):
							previous = current
							current = current.next 											#solo se mueve hasta encontrar el mayor.
						elif(compare.compare(current.name,name)>0):
							#entonces el nuevo valor va antes que el current
							#este guarda despues del actual
							previous.next = Node(value,name,typeDate,father,tabulated)
							previous.next.next = current
							return True
						elif(compare.compare(current.name,name) == 0):
							if(current.typeDate != typeDate):
								previous.next = Node(value,name,typeDate,father,tabulated)
								previous.next.next = current
							return True   
					previous.next = Node(value,name,typeDate,father,tabulated)
					return True

		elif(state == False):
			if(not self.first):
				self.first = Node(value,name,typeDate,father,tabulated)
		
			else:
				current = self.first
				while(current.next):
					current = current.next
				current.next = Node(value,name,typeDate,father,tabulated)
	#Buscar en la lista.
	def searchInLL(self,value,state = 0):			#Busqueda de un elemento, state =0 para devolver el nodo, state = 1 para regresar un boolean
		current = self.first
		if(state == 0):
			if(self.first.value == value):
				return self.first
			else:
				while (current.next):
					current = current.next
					if(current != None):
						if (current.value == value):
							return current
		
		elif(state == 1):
			if(current.value == value):
				return True
			else:
				while (current.next):
					current = current.next
					if (current.value == value):
						return True
				return False
	
	#Obtiene el ultimo elemento de la lista.
	def getLast(self):
		last = self.first
		while(last.next):
			last = last.next
		return last
	
	#Obtener el tamano de la lista.
	def length(self):
		current = self.first
		if(current !=None):
			size = 1
			while(current.next):
				current = current.next
				size += 1
			return size
		else:
			return 0

	#Obtener un item dado un indice.
	def atPosition(self,index):
		tam = self.length()
		current = self.first
		if(index >= tam):
			print("busqueda fuera de rango")
			return -1
		else:
			if(index == 0):
				return current
			else:
				count = 0
				while(current.next):
					current = current.next
					count +=1
					if(count == index):
						return current

	#Elimina elementos nodos dado su valor.
	def removeToNormal(self,value):					
		current = self.first
		if(current.value == value):
			self.first = current.next
		else:
			while(current.next):
				previous = current
				current = current.next
				if(current.value == value):
					previous.next = current.next
		
	#Remueve un elemento dado el nombre y el tipo de dato de este.
	def removeForNameAndType(self,name,intType):
		tempNode = self.searchItemForNameAndType(name,intType,1)
		if(tempNode != False):
			self.removeToNormal(tempNode.value)
			
			
	#Imprime los elementos de la lista	
	def _printToNormal(self,state = None):						
		current = self.first
		if(current != None):
			while (current.next):
				if(state==1):
					print(current)
				else:
					print (current.name)
				current = current.next
			if(state == 1):
				print(current)
			else:
				print (current.name)
		else:
			return None


	#Esta funcion sera al momento de verificar si puede agregar o no, un elemento si ya existe uno.		
	def searchItemForNameAndType(self,name,intType,state = 0):		#state==0 si solo queire que retorne boolean, '1' si quiere que retorne el nodo.
		current = self.first
		size = self.length()
		if(size != 0):
			for i in range(size):
				item = self.atPosition(i)
				if(item.name == name and item.typeDate == intType):
					if(state ==0):
						return True
					if(state == 1):
						return item
		return False				

	#Extrae los elementos por tipos.
	def extractForType(self):
		size = self.length()
		listDir = []
		listFile = []
		for i in range(size):
			item = self.atPosition(i)
			if(item.typeDate == 1):
				listDir.append(item)
			if(item.typeDate == 2):
				listFile.append(item)

		self.first = None

		return listDir,listFile

	#Ordena la LL por directorios
	def sortLL(self):
		listDir,listFile = self.extractForType()		#Lista de Directorios
		for j in range(len(listFile)):
			listDir.append(listFile[j])

		for i in range(len(listDir)):
			tab = listDir[i].tabulated
			parent = listDir[i].father
			children = listDir[i].children
			self.add(listDir[i].value,listDir[i].name,listDir[i].typeDate,parent,tab,False)
			self.searchInLL(listDir[i].value).children = children		
