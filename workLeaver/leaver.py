# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime as dt
import win32com.client as win32  
import urllib.request
import ssl
import os
import math
import json
import sys

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
			attachment = url.url().strip('file:///')
			self.addItem(attachment)

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		# glob variables 
		self.version = "v2.7.0"
		self.FMT = "%Y-%m-%d %H:%M:%S"
		self.today = dt.datetime.today()
		self.weekday = self.today.weekday()
		self.weekendSync = False
		self.isWeekend = self.checkIsWeekend()
		self.timeStartOfDay = self.convertTime("08:30:00")
		self.timeEndOfDay = self.convertTime("17:45:00")
		self.isLate = self.timeStartOfDay < dt.datetime.now() < self.timeEndOfDay
		self.isBeforeStart = dt.datetime.now() < self.timeStartOfDay
		self.timeStartOfExtra = None
		self.timeFinishOfExtra = None
		self.timeDelta = None
		self.timeDeltaLate = None
		self.timeDeltaBefore = None
		self.workForFree = ""
		self.logFile = self.getLogFile()
		############################################
		Dialog.setObjectName("Dialog")
		Dialog.setWindowModality(QtCore.Qt.NonModal)
		Dialog.setFixedSize(365, 370)
		self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(7, 3, 350, 360))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
		self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget)
		self.timeEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit.setObjectName("timeEdit")
		self.timeEdit.setEnabled(self.isWeekend)
		self.gridLayout.addWidget(self.timeEdit, 3, 1, 1, 2)
		self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText("Отправить письмо")
		self.pushButton.clicked.connect(self.sendMessage)
		self.gridLayout.addWidget(self.pushButton, 4, 2, 1, 1)
		self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
		self.textEdit.setObjectName("textEdit")
		font = QtGui.QFont()
		font.setPointSize(10)
		self.textEdit.setFont(font)
		self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)
		self.checkBox_2 = QtWidgets.QCheckBox(self.gridLayoutWidget)
		self.checkBox_2.setObjectName("checkBox_2")
		self.checkBox_2.stateChanged.connect(self.sorryImLate)
		self.checkBox_2.setEnabled(not self.isWeekend if self.isWeekend else self.isLate)
		self.gridLayout.addWidget(self.checkBox_2, 4, 0, 1, 1)
		self.checkBox_3 = QtWidgets.QCheckBox(self.gridLayoutWidget)
		self.checkBox_3.setObjectName("checkBox_3")
		self.checkBox_3.setEnabled(not self.isWeekend if self.isWeekend else self.isBeforeStart)
		self.checkBox_3.stateChanged.connect(self.earlyBirdy)
		self.gridLayout.addWidget(self.checkBox_3, 4, 1, 1, 1)
		self.informationLabel = QtWidgets.QLabel(self.gridLayoutWidget)
		self.informationLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.informationLabel.setObjectName("informationLabel")
		self.gridLayout.addWidget(self.informationLabel, 1, 0, 1, 3)
		self.listWidget = DragAndDropList(self.gridLayoutWidget)
		self.listWidget.setObjectName("listWidget")
		self.gridLayout.addWidget(self.listWidget,6,0,3,2)
		self.pushButton1 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton1.setObjectName("pushButton1")
		self.pushButton1.setText("+")
		self.pushButton1.clicked.connect(self.addAttachment)
		self.gridLayout.addWidget(self.pushButton1,6,2,1,1)
		self.pushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton2.setObjectName("pushButton2")
		self.pushButton2.setText("-")
		self.pushButton2.clicked.connect(self.removeAttachment)
		self.gridLayout.addWidget(self.pushButton2,7,2,1,1)
		self.pushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton3.setObjectName("pushButton3")
		self.pushButton3.setText("Очистить")
		self.pushButton3.clicked.connect(self.clearAttachment)
		self.gridLayout.addWidget(self.pushButton3,8,2,1,1)
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "WorQt %s" %self.version))
		self.timeEdit.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))
		self.pushButton.setText(_translate("Dialog", "Отправить"))
		self.pushButton1.setText(_translate("Dialog", "+"))
		self.pushButton2.setText(_translate("Dialog", "-"))
		self.pushButton3.setText(_translate("Dialog", "Очистить"))
		self.checkBox_2.setText(_translate("Dialog", "Пришел позже 8:30"))
		self.checkBox_3.setText(_translate("Dialog", "Пришел раньше 8:30"))
		self.label.setText(_translate("Dialog", "Начало рабочего дня"))

	def convertTime(self, stringTime):
		out = dt.datetime.strptime("%s %s" %(self.today.date(),stringTime), self.FMT)
		return out

	# def genVersionConfig(self):
	# 	file = '\\ver.conf'
	# 	with open(file,'bw') as config:
	# 		values = {"version":self.version}
	# 		json.dump(values,config)

	# def checkForUpdate(self):
	# 	try:
	# 		fileName = '\\ver.conf'
	# 		with open(fileName,'br') as config:
	# 			configVersion = json.load(config)
	# 		version = configVersion['Version']
	# 		verCurrent = self.version.split('.')
	# 		verToCheck = version.split('.')
	# 		for index in range(len(verCurrent)):
	# 			if verCurrent[index] < verToCheck[index]:
	# 				QtWidgets.QMessageBox.about(self,'Обновление','Доступна новая версия %s'%version)
	# 				break
	# 			else: continue
	# 	except Exception as ex:
	# 		self.writeLog('addAttachment failed with %s' %ex)

	def addAttachment(self, parent):
		try:
			attachments = QtWidgets.QFileDialog.getOpenFileUrls()[0]
			for url in attachments:
				attachment = url.url().strip('file:///')
				self.listWidget.addItem(attachment)
		except Exception as ex:
			self.writeLog('addAttachment failed with %s' %ex)

	def removeAttachment(self, parent):
		try: #https://stackoverflow.com/questions/23835847/how-to-remove-item-from-qlistwidget/23836142
			listItems = self.listWidget.selectedItems()
			if not listItems: return
			for item in listItems:
				self.listWidget.takeItem(self.listWidget.row(item))
		except Exception as ex:
			self.writeLog('removeAttachment failed with %s' %ex)
	
	def clearAttachment(self, parent):
		try: self.listWidget.clear()
		except Exception as ex:
			self.writeLog('clearAttachment failed with %s' %ex)

	def sorryImLate(self):
		flag = self.checkBox_2.checkState()
		self.checkBox_3.setEnabled(not flag)

	def earlyBirdy(self,parent):
		flag = self.checkBox_3.checkState()
		self.checkBox_2.setEnabled(not flag)

	def checkIsWeekend(self):
		try:
			today = self.today.strftime("%Y%m%d")
			scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			chemeo_search_url = 'https://isdayoff.ru/%s' %today
			response = urllib.request.urlopen(chemeo_search_url, context = scontext, timeout = 5)
			response = int(response.read().decode('utf-8'))
			outVal = True if response in [1] else False
			self.weekendSync = True
		except:	outVal = True if self.weekday in [5,6] else False
		return outVal 

	def getTime(self, mode):
		try:
			if mode == 2:
				if dt.datetime.now() > self.timeEndOfDay:
					self.informationLabel.setText("Уже слишком поздно")
					return None
				else: self.timeDeltaLate = dt.datetime.now() - self.timeStartOfDay
				return True
			elif mode == 3:
				self.timeDeltaBefore = self.timeStartOfDay - dt.datetime.now()
				return True
			else:
				today = self.today.strftime("%d.%m.%Y")
				if self.isWeekend: self.timeStartOfExtra = dt.datetime.strptime("%s %s" %(today,self.timeEdit.text()), "%d.%m.%Y %H:%M:%S")
				elif self.weekday in [4]: self.timeStartOfExtra = self.convertTime("16:30:00")
				else:  self.timeStartOfExtra = self.timeEndOfDay
				self.timeFinishOfExtra = dt.datetime.now()
				self.timeDelta = self.timeFinishOfExtra - self.timeStartOfExtra
				if self.timeDelta < dt.timedelta(seconds = 1):
					self.informationLabel.setText("Рабочий день еще продолжается")
					return None
				if self.timeDelta > dt.timedelta(seconds = 1): 
					if self.isWeekend and self.timeDelta < dt.timedelta(hours = 4):
						self.workForFree = "Отработка меньше 4 часов в выходной"			
						return True
					if not(self.isWeekend) and self.timeDelta < dt.timedelta(hours = 1): 
						self.workForFree = "Отработка меньше 1 часа в в будний день"	
						return True
					return True
		except Exception as ex:
			self.writeLog('getTime failed with %s' %ex)
				
	def extractTimeFormat(self,tdelta):
		try:
			d = {}
			d['days'] = tdelta.days
			d['hrs'], rem = divmod(tdelta.seconds, 3600)
			d['min'], d['sec'] = divmod(rem, 60)
			for key,val in d.items():
				if d[key] < 10 : d[key] = "0%s"%(val)
			return ('%s:%s:%s' %(d['hrs'],d['min'],d['sec']))
		except Exception as ex:
			self.writeLog('extractTimeFormat failed with %s' %ex)

	def sendMessage(self, parent):
		try:
			today = self.today.strftime("%d.%m.%Y")
			if self.checkBox_2.checkState():
				if self.getTime(2) is None: return None
				subject = 'Выход на работу - %s' %today
				message = ['<br>%s</br>' %today,
							'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
							'<br>Пришел позже на : %s</br>' %self.extractTimeFormat(self.timeDeltaLate)]	
			elif self.checkBox_3.checkState():
				if self.getTime(3) is None: return None
				subject = 'Переработка - %s' %today
				message = ['<br>%s</br>' %today,
							'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
							'<br>Пришел раньше на : %s</br>' %self.extractTimeFormat(self.timeDeltaBefore)]	
			else:
				if self.getTime(1) is None: return None
				subject = 'Переработка - %s' %today
				text = (self.textEdit.toPlainText()).split('\n')
				activity = ['<br>%s</br>' %row for row in text]
				message = ['<br>%s</br>' %today,
							'<br>Ушел в : %s</br>' %self.timeFinishOfExtra.strftime('%H:%M:%S'),
							'<br>Переработано: %s</br>' %self.extractTimeFormat(self.timeDelta),
							'<br>Полных часов: %s ч</br>' %(math.floor(self.timeDelta.seconds / 3600)),
							'%s' %(''.join(activity)),'<br><b>%s<b></br>'%self.workForFree]
				if self.isWeekend: message.insert(1,'<br>Пришел в: %s</br>' %self.timeStartOfExtra.strftime('%H:%M:%S'))
			message = ''.join(message)
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = ''
			mail.CC = ''
			for i in range(self.listWidget.count()):
				attachment = self.listWidget.item(i).text()
				mail.Attachments.Add(attachment)
			mail.Subject = subject
			mail.GetInspector 
			index = mail.HTMLbody.find('>', mail.HTMLbody.find('<body')) 
			mail.HTMLbody = mail.HTMLbody[:index + 1] + message + mail.HTMLbody[index + 1:] 
			mail.Display(True)
			#mail.send #uncomment if you want to send instead of displaying
			#sys.exit(app.exec_())
			#else: sys.exit(app.exec_())
		except Exception as ex:
			self.writeLog('sendMessage failed with %s' %ex)

	def getLogFile(self):
		try:
			dirName = '%s\\worqt_cache' %os.environ['APPDATA']
			fileName = '%s\\worqt_cache\\log.txt' %os.environ['APPDATA']
			if os.path.isdir(dirName): pass
			else: os.mkdir(dirName)
			if os.path.isfile(fileName): return fileName 
			else: 
				with open(fileName,'a') as cache: 
					cache.close()
				return fileName
		except Exception as ex:
			self.writeLog('getLog failed with %s' %ex)
		
	def writeLog(self,logString):
		try:
			with open(self.logFile,'a') as log: 
					log.write('%s -- %s\n'%(dt.datetime.now(),logString))
			#import pyscreenshoot - slezhka
		except Exception as ex:
			#self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, 'writeCacheFile failed with %s' %ex)
			raise ex

def main(args):
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	# if 'generate_version_config' in args: ui.genVersionConfig()
	# ui.checkForUpdate()
	Dialog.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main(sys.argv)	
