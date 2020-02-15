import sys
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import PyQt5.QtCore as core
from Nucleo.Window import* 

class AppWindowPrincipal(QMainWindow):
    def __init__(self):
        super(AppWindowPrincipal,self).__init__()
        QMainWindow.__init__(self)

        self.ui = App()
        self.executionPrincipal()
        self.resize(200,100)

        QMainWindow.setWindowFlags(self, core.Qt.FramelessWindowHint)
        self.center()

    def executionPrincipal(self):
        self.labelTitle = QLabel()
        self.font = QFont()
        self.vLayout = QVBoxLayout()
        self.centralWidget = QWidget()
        
        self.font.setBold(True)
        self.labelTitle.setFont(self.font)
        self.labelTitle.setText("SELECT MULTIPLE APPLICATION")
        self.labelTitle.setAlignment(core.Qt.AlignHCenter | core.Qt.AlignVCenter)

        self.btnStart = QPushButton("C O N T I N U E ")
        self.btnStart.setFont(self.font)
        self.btnStart.setIcon(QIcon("Nucleo/Imagenes/start.png"))
        self.btnStart.setIconSize(core.QSize(80,80))

        self.movie = QMovie("Nucleo/Imagenes/Welcome.gif")
        self.gif = QLabel()
        self.gif.setMovie(self.movie)
        self.movie.start()


        self.btnExit = QPushButton("E  X  I  T")
        self.btnExit.setIcon(QIcon("Nucleo/Imagenes/exit.png"))
        self.btnExit.setIconSize(core.QSize(80, 80))
        self.btnExit.setFont(self.font)

        self.btnStart.clicked.connect(self.openWindow)
        self.btnExit.clicked.connect(self.exitApplication)

        self.btnStart.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.btnExit.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.vLayout.addWidget(self.labelTitle)
        self.vLayout.addWidget(self.gif)
        self.vLayout.addWidget(self.btnStart,2)
        self.vLayout.addWidget(self.btnExit,2)

        self.centralWidget.setLayout(self.vLayout)
        self.setCentralWidget(self.centralWidget)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(size.width()*3,size.height())

    def openWindow(self): 
        #self.ui.execution()
        self.ui.show()
        self.hide()
    
    def exitApplication(self):
        self.close()

    

