import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

class uygulama(QMainWindow):
    def __init__(self):
        super(uygulama, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle("Bitti")
        myFont = QtGui.QFont('MS Shell Dlg2',14)
        myFont.setBold(True)
        myFont.setPointSize(10)
        
        #Girişte
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Labirent Çözüldü")
        self.label1.setFixedSize(150, 50)
        self.label1.move(125, 50)
        self.label1.setFont(myFont)
        
        myFont.setPointSize(8)
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Toplam Süre: ")
        self.label2.setFixedSize(120 ,40)
        self.label2.move(125, 120)
        self.label2.setFont(myFont)
        
        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("Gezilen Kare Sayısı: ")
        self.label3.setFixedSize(160 ,40)
        self.label3.move(80, 160)
        self.label3.setFont(myFont)
        
        myFont.setPointSize(10)
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Kapat")
        self.button1.setFont(myFont)
        self.button1.clicked.connect(self.button_clicked_button1)
        self.button1.setFixedSize(100, 40)
        self.button1.move(150,220)
        
    def button_clicked_button1(self):
        self.setVisible(False)
    

def window():
    app = QApplication(sys.argv)
    win = uygulama()
    win.show()
    sys.exit(app.exec_())
        
        
        
        
        
        