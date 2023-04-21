from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QPushButton, QTableWidget, QMessageBox, QTableWidgetItem, QWidget, QVBoxLayout
import csv

class ColumnSelectionView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # assign default labels
        self.timeLabel = "timestamp"
        self.caseLabel = "case"
        self.eventLabel = "event"
        self.selected_column = 0
        self.selected_algorithm = 0

        # set up table widget
        self.table = QTableWidget(self)
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().sectionClicked.connect(self.__column_header_clicked)

        # set up column selector combo box
        self.column_selector = QComboBox(self)
        self.column_selector.setFixedSize(120, 20)
        self.column_selector.currentIndexChanged.connect(self.__column_selected)
        
        # set up algorithm selector combo box
        self.algorithm_selector = QComboBox(self)
        self.algorithm_selector.setFixedSize(120, 20)
        self.algorithm_selector.currentIndexChanged.connect(self.__algorithm_selected)

        # set up assign column buttons
        self.timeColumn_button = QPushButton('Assign to \nTimestamp', self)
        self.timeColumn_button.setFixedSize(100, 70)
        self.timeColumn_button.setStyleSheet("background-color: #ADD8E6;")
        self.timeColumn_button.clicked.connect(self.__assign_timeColumn)

        self.caseColumn_button = QPushButton('Assign to \nCase', self)
        self.caseColumn_button.setFixedSize(100, 70)
        self.caseColumn_button.setStyleSheet("background-color: #ADD8E6;")
        self.caseColumn_button.clicked.connect(self.__assign_caseColumn)

        self.eventColumn_button = QPushButton('Assign to \nEvent', self)
        self.eventColumn_button.setFixedSize(100, 70)
        self.eventColumn_button.setStyleSheet("background-color: #ADD8E6;")
        self.eventColumn_button.clicked.connect(self.__assign_eventColumn)

        # set up start import button
        self.start_import_button = QPushButton('Start Import', self)
        self.start_import_button.setFixedSize(80, 60)
        self.start_import_button.setStyleSheet("background-color: red;")
        self.start_import_button.clicked.connect(self.__start_import)

        # set up top layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.column_selector)
        top_layout.addWidget(self.timeColumn_button)
        top_layout.addWidget(self.caseColumn_button)
        top_layout.addWidget(self.eventColumn_button)
        top_layout.setAlignment(Qt.AlignLeft)
        top_layout.setSpacing(10)

        # set up selector and import button layout
        buttom_layout = QHBoxLayout()
        buttom_layout.addWidget(self.algorithm_selector)
        buttom_layout.addWidget(self.start_import_button)
        top_layout.setSpacing(10)

        # set up layout
        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(self.table)
        layout.addLayout(buttom_layout)

        # set up spacing and margins
        layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)

    def load_csv(self, filepath):
        with open(filepath, 'r') as file:
            # use csv.Sniffer() to try to detect the delimiter
            dialect = csv.Sniffer().sniff(file.read(1024))
            
            # reset the file pointer to the beginning of the file
            file.seek(0)
            
            # create a CSV reader using the detected dialect
            reader = csv.reader(file, dialect)

            headers = next(reader)
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.column_selector.addItems(headers)
            for row_index, row_data in enumerate(reader):
                self.table.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(col_data))

    def load_algorithms(self, array):
        for element in array:
            self.algorithm_selector.addItem(element)

    def __algorithm_selected(self, index):
        self.algorithm_selector.setCurrentIndex(index)
        self.selected_algorithm = index

    def __column_header_clicked(self, index):
        self.column_selector.setCurrentIndex(index)
        self.selected_column = index
    
    def __column_selected(self, index):
        self.selected_column = index

    def __assign_timeColumn(self):
        self.timeLabel = self.table.horizontalHeaderItem(self.selected_column).text()
        print(self.timeLabel + " assigned as time column")

    def __assign_caseColumn(self):
        self.caseLabel = self.table.horizontalHeaderItem(self.selected_column).text()
        print(self.caseLabel + " assigned as case column")

    def __assign_eventColumn(self):
        self.eventLabel = self.table.horizontalHeaderItem(self.selected_column).text()
        print(self.eventLabel + " assigned as event column")

    def clear(self):
        self.timeLabel = "timestamp"
        self.caseLabel = "case"
        self.eventLabel = "event"
        self.selected_column = 0
        self.column_selector.clear()

    def __start_import(self):
        msgBox = QMessageBox()
        msgBox.setText("Time label is "+self.timeLabel+"\n"+"Case label is "+self.caseLabel+"\n"+"Event label is "+self.eventLabel)
        msgBox.setInformativeText("Are these columns correct?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec_()

        if ret == QMessageBox.Cancel:
            return
        
        self.parent.display_mining_result(self.timeLabel, self.caseLabel, self.eventLabel, self.selected_algorithm)
    
