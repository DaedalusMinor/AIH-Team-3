import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from pandas import read_excel
import pandas as pd
import gps_model_tools
from folium.plugins import MarkerCluster

# Name of the HTML file to be generated
web_file = 'index.html'

# Number of data points to pull from excel file
MAX_MINUTES = 114
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout(self)

        self.webEngineView = QWebEngineView()
        self.loadPage()

        vbox.addWidget(self.webEngineView)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QWebEngineView')
        self.show()

    def loadPage(self):

        with open(web_file, 'r') as f:

            html = f.read()
            self.webEngineView.setHtml(html)

#df = read_excel('C:/Users/Daeda/Documents/Python WS/TippecanoeVisuals/LocationReport (25 Rendom 041120-061020.xlsx', parse_dates=True, nrows=MAX_MINUTES)
#clean_df = gps_model_tools.const_freq_transf(df['Location DateTime'].values, df['Latitude'].values, df['Longitude'].values)
#location = clean_df.values[:, 1:3]
m = folium.Map(location=[40.42, -86.9])
#for point in range(0, 60):
    #folium.Marker([location[point, 0], location[point,1]]).add_to(m)

#marker_cluster = MarkerCluster().add_to(m)
#for point in range(60, 108):
    #folium.Marker([location[point, 0], location[point,1]]).add_to(marker_cluster)
    
m.save(web_file)
app = QApplication(sys.argv)
ex = Example()
app.exec_()

