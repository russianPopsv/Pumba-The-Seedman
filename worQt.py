# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import csv
import os
import worQt_timer
import worQt_logger
import worQt_postman
import worQt_config

class DragAndDropList(QtWidgets.QListWidget):
	def __init__(self, parent=None, **args):
		super(DragAndDropList, self).__init__(parent, **args)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QtWidgets.QListWidget.InternalMove)

	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls():
			e.accept()
		else: e.ignore()

	def dropEvent(self, e):
		for url in e.mimeData().urls():
			attachment = url.url().strip("file:///")
			self.addItem(attachment)

class Ui_Dialog(QtWidgets.QDialog):
	def __init__(self,parent = None, **args):
		super(Ui_Dialog,self).__init__(parent,**args)
		self.version = "v3.2.0"
		self.config = ''#worQt_config.get_config()
		self.today = worQt_timer.get_today()
		self.is_weekend = worQt_timer.check_is_weekend(self.today)
		self.shutdown_time = 2700000
		self.file_log = ''#worQt_logger.get_file_log()
		self.init_shutdown_timer()
		self.workfolder = os.getcwd()

	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.setWindowTitle("WorQt {0}".format(self.version))
		Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint)
		Dialog.setWindowModality(QtCore.Qt.NonModal)
		Dialog.setFixedSize(355, 390)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.tabWidget = QtWidgets.QTabWidget(Dialog)
		self.tabWidget.setGeometry(QtCore.QRect(0, 0, 355, 390))
		self.tabWidget.setObjectName("tabWidget")
		#tab1
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.tabWidget.addTab(self.tab, "Editor")
		#
		self.gridLayoutWidget1 = QtWidgets.QWidget(self.tab)
		self.gridLayoutWidget1.setGeometry(QtCore.QRect(0, 0, 350, 360))
		self.gridLayoutWidget1.setObjectName("gridLayoutWidget1")
		#
		self.gridLayout1 = QtWidgets.QGridLayout(self.gridLayoutWidget1)
		self.gridLayout1.setContentsMargins(0, 0, 0, 0)
		self.gridLayout1.setObjectName("gridLayout1")
		#
		self.label = QtWidgets.QLabel(self.gridLayoutWidget1)
		self.label.setObjectName("label")
		self.label.setText("Weekend started at: ")
		self.gridLayout1.addWidget(self.label, 3, 0, 1, 1)
		#
		self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget1)
		self.timeEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit.setObjectName("timeEdit")
		self.timeEdit.setEnabled(self.is_weekend)
		self.timeEdit.setDisplayFormat("HH:mm:ss")
		self.gridLayout1.addWidget(self.timeEdit, 3, 1, 1, 1)
		#
		self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget1)
		self.textEdit.setObjectName("textEdit")
		self.textEdit.setFont(font)
		self.gridLayout1.addWidget(self.textEdit, 0, 0, 1, 3)
		#
		self.informationLabel = QtWidgets.QLabel(self.gridLayoutWidget1)
		self.informationLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.informationLabel.setObjectName("informationLabel")
		self.gridLayout1.addWidget(self.informationLabel, 1, 0, 1, 3)
		#
		self.widget_list = DragAndDropList(self.gridLayoutWidget1)
		self.widget_list.setObjectName("widget_list")
		self.gridLayout1.addWidget(self.widget_list, 6, 0, 3, 2)
		#
		self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText("Send")
		self.pushButton.clicked.connect(self.message_send_bind)
		self.gridLayout1.addWidget(self.pushButton, 4, 0, 1, 3)
		#
		self.pushButton1 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton1.setObjectName("pushButton1")
		self.pushButton1.setText("Add")
		self.pushButton1.clicked.connect(self.attachment_add)
		self.gridLayout1.addWidget(self.pushButton1, 6, 2, 1, 1)
		#
		self.pushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton2.setObjectName("pushButton2")
		self.pushButton2.setText("Remove")
		self.pushButton2.clicked.connect(self.attachment_remove)
		self.gridLayout1.addWidget(self.pushButton2, 7, 2, 1, 1)
		#
		self.pushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton3.setObjectName("pushButton3")
		self.pushButton3.setText("Clear all")
		self.pushButton3.clicked.connect(self.attachment_clear)
		self.gridLayout1.addWidget(self.pushButton3, 8, 2, 1, 1)
		#
		self.pushButton4 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton4.setObjectName("pushButton4")
		self.pushButton4.setText("Check in")
		self.pushButton4.setEnabled(self.is_weekend)
		self.pushButton4.clicked.connect(worQt_postman.message_send_extrwork_checkin)
		self.gridLayout1.addWidget(self.pushButton4, 3, 2, 1, 1)
		#
		#tab2
		self.tab_statistics = QtWidgets.QWidget()
		self.tab_statistics.setObjectName("tab_statistics")
		self.tabWidget.addTab(self.tab_statistics, "Statistics")
		#
		self.gridLayoutWidget2 = QtWidgets.QWidget(self.tab_statistics)
		self.gridLayoutWidget2.setGeometry(QtCore.QRect(0, 0, 350, 360))
		self.gridLayoutWidget2.setObjectName("gridLayoutWidget2")
		#
		self.gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget2)
		self.gridLayout2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout2.setObjectName("gridLayout2")
		#
		self.pushButton7 = QtWidgets.QPushButton(self.gridLayoutWidget2)
		self.pushButton7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton7.setObjectName("pushButton7")
		self.pushButton7.setText("Refresh")
		self.pushButton7.clicked.connect(self.fillview)
		self.gridLayout2.addWidget(self.pushButton7, 0, 0, 1, 1)
		#
		self.pushButton8 = QtWidgets.QPushButton(self.gridLayoutWidget2)
		self.pushButton8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton8.setObjectName("pushButton8")
		self.pushButton8.setText("-----------------")
		self.pushButton8.clicked.connect(self.table_export)
		self.gridLayout2.addWidget(self.pushButton8, 0, 1, 1, 1)
		#
		self.tableWidget = QtWidgets.QTableWidget()
		self.tableWidget.setObjectName("tableView")
		self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		self.gridLayout2.addWidget(self.tableWidget, 1, 0, 1, 8)
		#
		#tab settings
		self.tab_settings = QtWidgets.QWidget()
		self.tab_settings.setObjectName("tab_settings")
		self.tabWidget.addTab(self.tab_settings, "Settings")
		#
		self.gridLayoutWidget3 = QtWidgets.QWidget(self.tab_settings)
		self.gridLayoutWidget3.setGeometry(QtCore.QRect(0, 0, 350, 360))
		self.gridLayoutWidget3.setObjectName("gridLayoutWidget3")
		#
		self.gridLayout3 = QtWidgets.QGridLayout(self.gridLayoutWidget3)
		self.gridLayout3.setContentsMargins(0, 0, 0, 0)
		self.gridLayout3.setObjectName("gridLayout3")
		#
		self.combo_day = QtWidgets.QComboBox(self.gridLayoutWidget3)
		self.combo_day.setObjectName("combo_day")
		for item in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
			self.combo_day.addItem(item)

		self.gridLayout3.addWidget(self.combo_day, 0, 0, 1, 1)
		#
		self.label_day_start = QtWidgets.QLabel(self.gridLayoutWidget3)
		self.label_day_start.setAlignment(QtCore.Qt.AlignCenter)
		self.label_day_start.setObjectName("label_day_start")
		self.label_day_start.setText("Day start at: ")
		self.gridLayout3.addWidget(self.label_day_start, 1, 0, 1, 1)
		#
		self.timeEdit_start = QtWidgets.QTimeEdit(self.gridLayoutWidget3)
		self.timeEdit_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit_start.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit_start.setObjectName("timeEdit_start")
		self.timeEdit_start.setDisplayFormat("HH:mm:ss")
		self.gridLayout3.addWidget(self.timeEdit_start, 1, 1, 1, 1)
		#
		self.label_day_finish = QtWidgets.QLabel(self.gridLayoutWidget3)
		self.label_day_finish.setAlignment(QtCore.Qt.AlignCenter)
		self.label_day_finish.setObjectName("label_day_finish")
		self.label_day_finish.setText("Day finish at: ")
		self.gridLayout3.addWidget(self.label_day_finish, 1, 2, 1, 1)
		#
		self.timeEdit_finish = QtWidgets.QTimeEdit(self.gridLayoutWidget1)
		self.timeEdit_finish.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit_finish.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit_finish.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit_finish.setObjectName("timeEdit_finish")
		self.timeEdit_finish.setDisplayFormat("HH:mm:ss")
		self.gridLayout3.addWidget(self.timeEdit_finish, 1, 3, 1, 1)
		# self.fillview()

		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def init_shutdown_timer(self):
		self._shutdown_timer = QtCore.QTimer(self)
		self._shutdown_timer.setSingleShot(True)
		self._shutdown_timer.timeout.connect(sys.exit)
		self._shutdown_timer.start(self.shutdown_time)

	#attachment section
	def attachment_add(self, parent):
		try:
			attachments = QtWidgets.QFileDialog.getOpenFileUrls()[0]
			for url in attachments:
				attachment = url.url().strip("file:///")
				self.widget_list.addItem(attachment)
		except Exception as ex:
			worQt_logger.log_dump_crash()

	def attachment_remove(self, parent):
		try:
			list_items = self.widget_list.selectedItems()
			if not list_items: return
			for item in list_items:
				index = self.widget_list.row(item)
				self.widget_list.takeItem(index)
		except Exception as ex:
			worQt_logger.log_dump_crash()

	def attachment_clear(self, parent):
		try: self.widget_list.clear()
		except Exception as ex:
			worQt_logger.log_dump_crash()

	def message_send_bind(self):
		td = worQt_postman.message_send_extrawork(self.today)
		self.textEdit.setText(str(td))


	def check_in_bind(self):
		pass

	def fillview(self):#csv or json
		pass
		# try:
		# 	self.tableWidget.setColumnCount(0)
		# 	self.tableWidget.setRowCount(0)
		# 	connection = sqlite3.connect(self.file_log)
		# 	cursor = connection.cursor()
		# 	cursor.execute('''SELECT date_ as "Дата", 
		# 					session_start as "Начало смены",
		# 					session_end as "Конец смены",
		# 					duration as "Всего отработано",
		# 					duration_full as "Полных часов",
		# 					index_ as "Коэффициент"
		# 					FROM session_log''')
		# 	names = list(map(lambda x: x[0], cursor.description))
		# 	[self.tableWidget.insertColumn(i) for i in range(len(names))]
		# 	for row, form in enumerate(cursor):
		# 		self.tableWidget.insertRow(row)
		# 		for column, item in enumerate(form):
		# 			# self.tableWidget.insertColumn(column)
		# 			self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
		# 	self.tableWidget.setHorizontalHeaderLabels(names)
		# 	connection.close()
		# except Exception as ex:
		# 	connection.close()
		# 	worQt_logger.log_dump_crash()

	def table_export(self):
		destination = QtWidgets.QFileDialog.getExistingDirectoryUrl()
		try:
			file_log = self.file_log
			fileOutput = sys.argv[2]
			inputFile = open(fileInput) #open json file
			outputFile = open(fileOutput, 'w') #load csv file
			data = json.load(inputFile) #load json content
			inputFile.close() #close the input file
			output = csv.writer(outputFile) #create a csv.write
			output.writerow(data[0].keys())  # header row
			for row in data:
				output.writerow(row.values()) #values row
		except: pass #unstable sorry 
		pass

def main():
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	Dialog.show()
	app.exec_()

if __name__ == "__main__":
	main()
