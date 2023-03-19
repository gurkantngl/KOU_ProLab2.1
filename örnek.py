import sys
from PyQt5 import QtWidgets, QtGui
def click(pencere):
    print("Butona basıldı")
def Pencere():
    
    app = QtWidgets.QApplication(sys.argv)
    okay = QtWidgets.QPushButton("Tamam")
    cancel = QtWidgets.QPushButton("İptal")
    
    h_box = QtWidgets.QHBoxLayout()
    h_box.addWidget(okay)
    h_box.addWidget(cancel)
    h_box.addStretch()
    
    pencere = QtWidgets.QWidget()
    
    pencere.setLayout(h_box)
    
    pencere.setGeometry(300,300,800,600)
    okay.clicked.connect(click(pencere))
    pencere.show()
    
    
    sys.exit(app.exec_())
    
Pencere()