from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import os
import sys
import makememap

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        makememap.change_color_to_time()
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
            
        MainWindow.setEnabled(True)
        MainWindow.resize(955, 824)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 531, 521))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Add Map viewer to Verical Layout
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        url = QtCore.QUrl('http://127.0.0.1:8050/')
        ##QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'index.html'
        self.webEngineView.load(url)
        self.verticalLayout.addWidget(self.webEngineView)

        # Pressing button shows a dialog box
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QtCore.QRect(600, 100, 181, 31))
        

        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QtCore.QRect(590, 40, 261, 31))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QtCore.QRect(600, 180, 181, 31))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QtCore.QRect(600, 250, 181, 31))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QtCore.QRect(640, 520, 112, 32))
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.raise_()
        self.verticalLayoutWidget.raise_()
        self.horizontalSlider.raise_()
        self.pushButton_2.raise_()
        self.comboBox.raise_()
        self.pushButton_3.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 955, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_2, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.horizontalSlider)
        QWidget.setTabOrder(self.horizontalSlider, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.pushButton)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.show_dialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def show_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)

        x = msg.exec_()

    def selectionchange(self, i):
        ## S T R
        if i == 0:
            makememap.change_color_to_time()
        if i == 1:
            makememap.change_color_to_speed()
        if i == 2:
            makememap.change_color_to_risk()
    
        self.webEngineView.reload()
        

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", u"Toggle Outlier Selection", None))
        self.pushButton_2.setText(QtCore.QCoreApplication.translate("MainWindow", u"Toggle Trajectory", None))
        self.comboBox.setItemText(0, QtCore.QCoreApplication.translate("MainWindow", u"Time", None))
        self.comboBox.setItemText(1, QtCore.QCoreApplication.translate("MainWindow", u"Speed", None))
        self.comboBox.setItemText(2, QtCore.QCoreApplication.translate("MainWindow", u"Risk", None))
        self.comboBox.currentIndexChanged.connect(self.selectionchange)

        self.pushButton_3.setText(QtCore.QCoreApplication.translate("MainWindow", u"Refresh", None))
    # retranslateUi

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Window)
    Window.show()
    app.exec_()
