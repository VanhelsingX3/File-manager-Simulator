from Nucleo.inputWindow import*

if __name__ == "__main__": 
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("Nucleo/Imagenes/input.png"))
	window = AppWindowPrincipal()
	window.setWindowTitle("Select Multiple Application")
	window.show()
	sys.exit(app.exec_())