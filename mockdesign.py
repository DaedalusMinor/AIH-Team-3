from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import os
import sys
import makememap
import numpy
import random
import math
from math import *
import datetime
from datetime import timedelta
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace
from dash.dependencies import Input, Output
import time
import threading

map = None
print("mapap")
def makemap():
    map = makememap.Map(1440 * 10)

thread = threading.Thread(target=makemap)
thread.start()
print("mamapap")


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
            
        MainWindow.setEnabled(True)
        MainWindow.resize(900, 600)
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
        # url = QtCore.QUrl('http://127.0.0.1:8050/')
        # QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'index.html'
        self.webEngineView.load(QtCore.QUrl('http://127.0.0.1:8080/'))
        self.verticalLayout.addWidget(self.webEngineView)

        # Pressing button shows a dialog box
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QtCore.QRect(600, 240, 200, 30))

        # startDE objects, end and start time for time intervals
        self.startDE = QDateTimeEdit(self.centralwidget)
        self.startDE.setGeometry(600, 40, 200, 30)
        self.startDE.setMinimumDate(QtCore.QDate.currentDate().addDays(-365))
        self.startDE.setMaximumDate(QtCore.QDate.currentDate().addDays(365))
        self.startDE.setDisplayFormat("dd.MM.yyyy hh:mm")
        
        self.endDE = QDateTimeEdit(self.centralwidget)
        self.endDE.setGeometry(600, 100, 200, 30)
        self.endDE.setMinimumDate(QtCore.QDate.currentDate().addDays(-365))
        self.endDE.setMaximumDate(QtCore.QDate.currentDate().addDays(365))
        self.endDE.setDisplayFormat("dd.MM.yyyy hh:mm")

        # button to open analysis window, showing data from start to end time.
        self.showAnalysisBtn = QPushButton(self.centralwidget)
        self.showAnalysisBtn.setObjectName(u"showAnalysisBtn")
        self.showAnalysisBtn.setGeometry(QtCore.QRect(600, 160, 200, 30))
        self.showAnalysisBtn.clicked.connect(self.toggle_window)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QtCore.QRect(600, 200, 200, 30))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QtCore.QRect(600, 280, 200, 30))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QtCore.QRect(600, 509, 200, 30))
        self.pushButton_3.clicked.connect(self.refresh)
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.raise_()
        self.verticalLayoutWidget.raise_()
        # self.horizontalSlider.raise_()
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
        # QWidget.setTabOrder(self.comboBox, self.horizontalSlider)
        # QWidget.setTabOrder(self.horizontalSlider, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.pushButton)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.show_dialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.w = AnotherWindow()
    
    def showAnalysisWindow(self):
        start = self.startDE.dateTime().toPyDateTime()
        end = self.endDE.dateTime().toPyDateTime()
        print(map.get_time_interval(start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")))


    def show_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        x = msg.exec_()

    def refresh(self):
        self.webEngineView.reload()

    def selectionchange(self, i):
        ## T S R
        if i == 0:
            map.change_color_to_time()
        if i == 1:
            map.change_color_to_speed()
        if i == 2:
            map.change_color_to_risk()
    
        self.webEngineView.reload()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("Main Window", u"Main Window", None))
        self.showAnalysisBtn.setText(QtCore.QCoreApplication.translate("MainWindow", u"Show Analysis Window", None))
        self.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", u"Toggle Outlier Selection", None))
        self.pushButton_2.setText(QtCore.QCoreApplication.translate("MainWindow", u"Toggle Trajectory", None))
        self.comboBox.setItemText(0, QtCore.QCoreApplication.translate("MainWindow", u"Time", None))
        self.comboBox.setItemText(1, QtCore.QCoreApplication.translate("MainWindow", u"Speed", None))
        self.comboBox.setItemText(2, QtCore.QCoreApplication.translate("MainWindow", u"Risk", None))
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.pushButton_3.setText(QtCore.QCoreApplication.translate("MainWindow", u"Refresh", None))
    # retranslateUi

    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView()
        # url = QtCore.QUrl('http://127.0.0.1:8050/')
        # QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'index.html'
        self.webEngineView.load(QtCore.QUrl('http://127.0.0.1:8050/'))
        layout.addWidget(self.webEngineView)


def run():
    # defining the number of steps 
    n = 500

    #creating two array for containing x and y coordinate 
    #of size equals to the number of size and filled up with 0's 
    x = numpy.zeros(n)
    y = numpy.zeros(n)
    global locations

    locations = [] #used in map generator
    locations_base = [] #the base data.
    start_location=[40.4259, -86.9081]
    at_risk = numpy.random.uniform(low=0.0, high=1.1, size=(n,))
    start_time = 0
    map_dir = "index.html"
    MINUTES_IN_DAY = 1440
    start_date = datetime.datetime.now()

    times = list(range(0, n))
    time_index = 0
    datetimes = []

    for i in range(len(times)):
        noise = random.randint(1,5)
        times[i] = (times[i] + noise)
        datetimes.append(start_date + timedelta(minutes=times[i]))

    datetimeindex = pd.Series(range(0, n), index=datetimes)

    #filling the coordinates with random variables 
    for i in range(1, n): 
        val = random.randint(1, 4) 
        if val == 1: 
            x[i] = x[i - 1] + 0.001
            y[i] = y[i - 1] 
        elif val == 2: 
            x[i] = x[i - 1] - 0.001
            y[i] = y[i - 1]
        elif val == 3: 
            x[i] = x[i - 1]
            y[i] = y[i - 1] + 0.001
        else: 
            x[i] = x[i - 1]
            y[i] = y[i - 1] - 0.001
        locations_base.append([x[i] + start_location[0], y[i] + start_location[1]])

    ns = Namespace("dlx", "scatter")

    new_markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{times[i]}"), 
        position=pos, 
        id="marker{}".format(i)) for i, pos in enumerate(locations)]

    cluster = dl.MarkerClusterGroup(id="new_markers", 
        children=new_markers, 
        options={"polygonOptions": {"color": "red"}})

    patterns = [dict(offset='0%', repeat='0', marker={})]
    polyline = dl.Polyline(positions=[locations],id="id_polyline")
    marker_pattern = dl.PolylineDecorator(id="id_marker_pattern", children=polyline, patterns=patterns)

    app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
    app.layout = html.Div(
        html.Div([
            dl.Map([dl.TileLayer(), cluster, marker_pattern, dl.LayerGroup(id="layer")],
            id="map",
            center=(40.4259, -86.9081), zoom=8, style={'height': '100vh'}),
            #html.Div(id='live-update-text'),
            dcc.Interval(
                id="interval",
                interval=1*1000, # in milliseconds
                n_intervals=0)
        ])
    )

    @app.callback(Output('id_marker_pattern','children'), [Input('interval','n_intervals')])
    def update_polyline(b):
        polyline = dl.Polyline(positions=locations)
        return polyline

    @app.callback(Output('new_markers','children'), [Input('interval', 'n_intervals')])
    def update_metrics(a):

        locations.append([locations_base[a][0], locations_base[a][1]])
        if(len(locations) >= 100):
            locations.pop(0)
        new_markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{times[i]}"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(locations)]
        return new_markers

    def rgb_to_hex(rgb):
        return ('%02x%02x%02x' % rgb)

    def get_time_interval(sd, ed):
        indices = datetimeindex[sd:ed].to_numpy()
        print(indices)

    def change_color_to_time():
        for i in range(len(locations)):
            time = times[i]
            r = 255 - math.trunc(255 * (time / MINUTES_IN_DAY))
            color_tuple = (r, r, r)
            rgb = rgb_to_hex(color_tuple)
            icon = {
                "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
                "iconSize": [20, 30],  # size of the icon
            }
            markers[i].icon = icon
        

    def change_color_to_risk():
        for i in range(len(locations)):
            time = times[i]
            risk = math.trunc(at_risk[i])            
            if (risk == 1):
                icon = {
                    "iconUrl": "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FF0000&chf=a,s,ee00FFFF",
                    "iconSize": [20, 30],  # size of the icon
                }
            else:
                icon = {
                    "iconUrl": "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|00FF00&chf=a,s,ee00FFFF",
                    "iconSize": [20, 30],  # size of the icon
                }
            markers[i].icon = icon
            print("risk")

    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    def change_color_to_speed():
        speed=0
        avewalk=0.084
        speeddiff=0
            
        for i in range(len(locations)):
            if i == 0:
                speed=0
            elif (times[i]-times[i-1])==0:
                speed=0
            else:
                #coords_1 = [locations[i][0], locations[i][1]]
                #coords_2 = [locations[i-1][0], locations[i-1][1]]
                #distance = h3.point_dist(coords_1,coords_2)
                R = 6373.0
                lat1 = radians(locations[i][0])
                lon1 = radians(locations[i][1])
                lat2 = radians(locations[i-1][0])
                lon2 = radians(locations[i-1][1])
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = 2
                ##sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 
                ##2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                speed = abs(distance / (times[i]-times[i-1]))
            
            speeddiff=speed*1000/60 - 1.4
            r=clamp(100+speeddiff*300,0,255)    #grey normal, yellow fast, blue slow
            g=clamp(100+speeddiff*100,0,255)
            b=clamp(100-speeddiff*100,0,255)
            color_tuple = (int(r), int(g), int(b))
            rgb = rgb_to_hex(color_tuple)
            icon = {
                "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
                "iconSize": [20, 30],  # size of the icon
            }
            markers[i].icon = icon
    app.run_server(port=8050)

if __name__ == "__main__":
    thread = threading.Thread(target=run)
    thread.start()
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Window)
    Window.show()
    app.exec_()
