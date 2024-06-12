import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QLabel, QDesktopWidget, QSizePolicy
from PyQt5.QtCore import Qt
from heatmap import dataBasedCrimeHeatmap
from graph import dataBasedCrimeGraph
from PyQt5.QtGui import QPixmap

CODES = {'Albania': 'ALB', 'Algeria': 'DZA', 'Andorra': 'AND', 'Antigua and Barbuda': 'ATG', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Australia': 'AUS', 'Austria': 'AUT', 'Azerbaijan': 'AZE', 'Bahamas': 'BHS', 'Bahrain': 'BHR', 'Bangladesh': 'BGD', 'Barbados': 'BRB', 'Belarus': 'BLR', 'Belgium': 'BEL', 'Belize': 'BLZ', 'Benin': 'BEN', 'Bermuda': 'BMU', 'Bhutan': 'BTN', 'Bolivia (Plurinational State of)': 'BOL', 'Bosnia and Herzegovina': 'BIH', 'Botswana': 'BWA', 'Brazil': 'BRA', 'Brunei Darussalam': 'BRN', 'Bulgaria': 'BGR', 'Burundi': 'BDI', 'Cabo Verde': 'CPV', 'Cameroon': 'CMR', 'Canada': 'CAN', 'Chile': 'CHL', 'China': 'CHN', 'China, Hong Kong Special Administrative Region': 'HKG', 'China, Macao Special Administrative Region': 'MAC', 'Colombia': 'COL', 'Costa Rica': 'CRI', 'Croatia': 'HRV', 'Cyprus': 'CYP', 'Czechia': 'CZE', 'Côte d’Ivoire': 'CIV', 'Denmark': 'DNK', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Dominican Republic': 'DOM', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'El Salvador': 'SLV', 'Estonia': 'EST', 'Eswatini': 'SWZ', 'Finland': 'FIN', 'France': 'FRA', 'Georgia': 'GEO', 'Germany': 'DEU', 'Greece': 'GRC', 'Grenada': 'GRD', 'Guatemala': 'GTM', 'Guinea': 'GIN', 'Guinea-Bissau': 'GNB', 'Guyana': 'GUY', 'Holy See': 'VAT', 'Honduras': 'HND', 'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IND', 'Indonesia': 'IDN', 'Iran (Islamic Republic of)': 'IRN', 'Iraq (Central Iraq)': 'IRQ_C', 'Ireland': 'IRL', 'Israel': 'ISR', 'Italy': 'ITA', 'Jamaica': 'JAM', 'Japan': 'JPN', 'Jordan': 'JOR', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kosovo under UNSCR 1244': 'XKX', 'Kuwait': 'KWT', 'Kyrgyzstan': 'KGZ', 'Latvia': 'LVA', 'Lebanon': 'LBN', 'Lesotho': 'LSO', 'Liechtenstein': 'LIE', 'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Madagascar': 'MDG', 'Malaysia': 'MYS', 'Maldives': 'MDV', 'Malta': 'MLT', 'Mauritius': 'MUS', 'Mexico': 'MEX', 'Monaco': 'MCO', 'Mongolia': 'MNG', 'Montenegro': 'MNE', 'Morocco': 'MAR', 'Mozambique': 'MOZ', 'Myanmar': 'MMR', 'Namibia': 'NAM', 'Nepal': 'NPL', 'Netherlands': 'NLD', 'New Zealand': 'NZL', 'Nicaragua': 'NIC', 'Nigeria': 'NGA', 'North Macedonia': 'MKD', 'Norway': 'NOR', 'Oman': 'OMN', 'Pakistan': 'PAK', 'Panama': 'PAN', 'Paraguay': 'PRY', 'Peru': 'PER', 'Philippines': 'PHL', 'Poland': 'POL', 'Portugal': 'PRT', 'Puerto Rico': 'PRI', 'Qatar': 'QAT', 'Republic of Korea': 'KOR', 'Republic of Moldova': 'MDA', 'Romania': 'ROU', 'Russian Federation': 'RUS', 'Rwanda': 'RWA', 'Saint Kitts and Nevis': 'KNA', 'Saint Lucia': 'LCA', 'Saint Vincent and the Grenadines': 'VCT', 'Sao Tome and Principe': 'STP', 'Saudi Arabia': 'SAU', 'Senegal': 'SEN', 'Serbia': 'SRB', 'Sierra Leone': 'SLE', 'Singapore': 'SGP', 'Slovakia': 'SVK', 'Slovenia': 'SVN', 'Solomon Islands': 'SLB', 'Spain': 'ESP', 'Sri Lanka': 'LKA', 'State of Palestine': 'PSE', 'Sudan': 'SDN', 'Suriname': 'SUR', 'Sweden': 'SWE', 'Switzerland': 'CHE', 'Syrian Arab Republic': 'SYR', 'Tajikistan': 'TJK', 'Thailand': 'THA', 'Timor-Leste': 'TLS', 'Trinidad and Tobago': 'TTO', 'Turkmenistan': 'TKM', 'Türkiye': 'TUR', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'United Arab Emirates': 'ARE', 'United Kingdom (England and Wales)': 'GBR_E_W', 'United Kingdom (Northern Ireland)': 'GBR_NI', 'United Kingdom (Scotland)': 'GBR_S', 'United Republic of Tanzania': 'TZA', 'United States of America': 'USA', 'Uruguay': 'URY', 'Uzbekistan': 'UZB', 'Venezuela (Bolivarian Republic of)': 'VEN', 'Yemen': 'YEM', 'Zimbabwe': 'ZWE'}
CRIMES = ["Corruption", "Corruption: Bribery", "Corruption: Other acts of corruption", "Smuggling of migrants", "Burglary", "Theft", "Theft: of a motorized vehicle", "Fraud", "Fraud: Cyber-related (Cy)", "Money laundering", "Unlawful access to a computer system", "Unlawful interference with a computer system or computer data", "Unlawful interception or access of computer data", "Acts that cause environmental pollution or degradation", "Acts involving the movement of dumping of waste", "Trade or possession of protected or prohibited species of fauna and flora", "Acts that result in the depletion of degradation of natural resources"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1200, 801)
        self.resetPosition()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.mainLayout = QVBoxLayout(self.central_widget)
        self.optionsLayout = QHBoxLayout()
        self.optionsLayout.setAlignment(Qt.AlignBottom)
        self.display = QLabel()
        self.mainLayout.addWidget(self.display, alignment=Qt.AlignBottom|Qt.AlignCenter)
        self.mainLayout.addLayout(self.optionsLayout)
        
        self.mainMenu()
        
    def mainMenu(self):
        self.clearWindow()
        if(hasattr(self, 'backButton')):
            self.mainLayout.itemAt(0).widget().deleteLater()
        
        self.resize(1200, 801)
        self.setWindowTitle('Crime Data Visualizer')
        
        mainPic = QPixmap("crime.jpeg")
        mainPic = mainPic.scaled(1200, 801, Qt.KeepAspectRatio)
        self.display.setPixmap(mainPic)
        
        self.graphButton = QPushButton("Draw Graph")
        self.graphButton.clicked.connect(self.graphMenu)
        self.optionsLayout.addWidget(self.graphButton)

        self.heatmapButton = QPushButton("Draw Heatmap")
        self.heatmapButton.clicked.connect(self.heatmapMenu)
        self.optionsLayout.addWidget(self.heatmapButton)
        
        self.mainLayout.update()
        self.resetPosition()
        
    def graphMenu(self):
        self.clearWindow()
        self.setWindowTitle('Heatmap drawer')
        self.display.setText("Choose the criteria for the graph:")
        
        self.startYearComboBox = QComboBox()
        self.endYearComboBox = QComboBox()
        self.fillYearCombo(self.startYearComboBox, 2003, 2021)
        self.fillYearCombo(self.endYearComboBox, 2004, 2021)
        self.startYearComboBox.currentIndexChanged.connect(lambda: self.fillYearCombo(self.endYearComboBox, int(self.startYearComboBox.currentText()) + 1, 2021))
        self.optionsLayout.addWidget(self.startYearComboBox)
        self.optionsLayout.addWidget(self.endYearComboBox)
        
        self.countryComboBox = QComboBox()
        self.countryComboBox.addItems(CODES.keys())
        self.optionsLayout.addWidget(self.countryComboBox)
        
        self.crimeComboBox = QComboBox()
        self.fillListCombo(self.crimeComboBox, CRIMES)
        self.optionsLayout.addWidget(self.crimeComboBox)
        
        self.measurementComboBox = QComboBox()
        self.measurementComboBox.addItem("Counts")
        self.measurementComboBox.addItem("Rate per 100,000 population")
        self.optionsLayout.addWidget(self.measurementComboBox)
        
        self.drawGraphButton = QPushButton("Draw Graph")
        self.drawGraphButton.clicked.connect(self.displayGraph)
        self.optionsLayout.addWidget(self.drawGraphButton)
        
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.mainMenu)
        self.mainLayout.insertWidget(0, self.backButton, alignment=Qt.AlignLeft|Qt.AlignTop)
        self.resetPosition()

    def heatmapMenu(self):
        self.clearWindow()
        self.setWindowTitle('Heatmap drawer')
        pic = QPixmap("blankmap.jpeg")
        pic = pic.scaled(1200, 801, Qt.KeepAspectRatio)
        self.display.setPixmap(pic)
        
        
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.mainMenu)
        self.mainLayout.insertWidget(0, self.backButton, alignment=Qt.AlignLeft|Qt.AlignTop)
        
        self.yearComboBox = QComboBox()
        self.fillYearCombo(self.yearComboBox, 2003, 2021)
        self.optionsLayout.addWidget(self.yearComboBox)

        self.regionComboBox = QComboBox()
        self.regionComboBox.addItem("All")
        self.regionComboBox.addItem("Europe")
        self.regionComboBox.addItem("Asia")
        self.regionComboBox.addItem("Africa")
        self.regionComboBox.addItem("Americas")
        self.optionsLayout.addWidget(self.regionComboBox)

        self.crimeComboBox = QComboBox()
        self.fillListCombo(self.crimeComboBox, CRIMES)
        self.optionsLayout.addWidget(self.crimeComboBox)

        self.measurementComboBox = QComboBox()
        self.measurementComboBox.addItem("Counts")
        self.measurementComboBox.addItem("Rate per 100,000 population")
        self.optionsLayout.addWidget(self.measurementComboBox)

        self.heatmapButton = QPushButton("Display Heatmap")
        self.heatmapButton.clicked.connect(self.displayHeatmap)
        self.optionsLayout.addWidget(self.heatmapButton)
        self.mainLayout.update()
        self.resetPosition()


    def displayHeatmap(self):
        year = int(self.yearComboBox.currentText())
        region = self.regionComboBox.currentText()
        crime = self.crimeComboBox.currentText()
        measurement = self.measurementComboBox.currentText()
        try:
            dataBasedCrimeHeatmap(year, crime, region, measurement)
            pic = QPixmap("heatmap.jpeg")
            pic = pic.scaled(1200, 1200, Qt.KeepAspectRatio)
            self.display.setPixmap(pic)
            self.resetPosition()
        except Exception as e:
            print(e)
            self.error = QMessageBox()
            self.error.setIcon(1)
            self.error.setWindowTitle("No data found")
            self.error.setText("There was no data found for this combination of criteria.")
            self.error.exec()
            
            
    def displayGraph(self):
        startYear = int(self.startYearComboBox.currentText())
        endYear = int(self.endYearComboBox.currentText())
        country = self.countryComboBox.currentText()
        crime = self.crimeComboBox.currentText()
        measure = self.measurementComboBox.currentText()
        try:
            isFull = dataBasedCrimeGraph(startYear, endYear, crime, country, measure)
            pic = QPixmap("graph.jpeg")
            pic = pic.scaled(2400, 950, Qt.KeepAspectRatio)
            self.display.setPixmap(pic)
            self.resetPosition()
            if(isFull == False):
                self.error = QMessageBox()
                self.error.setIcon(1)
                self.error.setWindowTitle("Incomplete data")
                self.error.setText("Some years might be missing because no data was found for those years")
                self.error.exec()
        except Exception as e:
            print(e)
            self.error = QMessageBox()
            self.error.setIcon(1)
            self.error.setWindowTitle("No data found")
            self.error.setText("There was no data found for this combination of criteria.")
            self.error.exec()
    
    
    def clearWindow(self):
        while self.optionsLayout.count():
            child = self.optionsLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def resetPosition(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
                
                
    def fillYearCombo(self, comboBox: QComboBox, startYear: int, endYear: int):
        comboBox.clear()
        for i in range(startYear, endYear):
            comboBox.addItem(str(i))
        comboBox.update()
        
    def fillListCombo(self, comboBox: QComboBox, lis: list):
        comboBox.clear()
        comboBox.addItems(lis)
        comboBox.update()
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())