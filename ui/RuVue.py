# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RuVue.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rbn_run = QtWidgets.QPushButton(self.centralwidget)
        self.rbn_run.setGeometry(QtCore.QRect(80, 120, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.rbn_run.setFont(font)
        self.rbn_run.setObjectName("rbn_run")
        self.rbn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.rbn_exit.setGeometry(QtCore.QRect(200, 120, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.rbn_exit.setFont(font)
        self.rbn_exit.setObjectName("rbn_exit")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(50, 20, 101, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 20, 81, 61))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rbn_Tx = QtWidgets.QRadioButton(self.widget)
        self.rbn_Tx.setObjectName("rbn_Tx")
        self.verticalLayout.addWidget(self.rbn_Tx)
        self.rbn_Rx = QtWidgets.QRadioButton(self.widget)
        self.rbn_Rx.setObjectName("rbn_Rx")
        self.verticalLayout.addWidget(self.rbn_Rx)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(170, 20, 131, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget1 = QtWidgets.QWidget(self.groupBox_2)
        self.widget1.setGeometry(QtCore.QRect(10, 20, 101, 61))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.rbn_A = QtWidgets.QRadioButton(self.widget1)
        self.rbn_A.setObjectName("rbn_A")
        self.gridLayout.addWidget(self.rbn_A, 0, 0, 1, 1)
        self.rbn_C = QtWidgets.QRadioButton(self.widget1)
        self.rbn_C.setObjectName("rbn_C")
        self.gridLayout.addWidget(self.rbn_C, 0, 1, 1, 1)
        self.rbn_B = QtWidgets.QRadioButton(self.widget1)
        self.rbn_B.setObjectName("rbn_B")
        self.gridLayout.addWidget(self.rbn_B, 1, 0, 1, 1)
        self.rbn_D = QtWidgets.QRadioButton(self.widget1)
        self.rbn_D.setObjectName("rbn_D")
        self.gridLayout.addWidget(self.rbn_D, 1, 1, 1, 1)
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(340, 20, 821, 741))
        self.graphWidget.setObjectName("graphWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 190, 41, 9))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.rbn_exit.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RuVue"))
        self.rbn_run.setText(_translate("MainWindow", "Run"))
        self.rbn_exit.setText(_translate("MainWindow", "Cancel"))
        self.groupBox.setTitle(_translate("MainWindow", "Case"))
        self.rbn_Tx.setText(_translate("MainWindow", "Tx"))
        self.rbn_Rx.setText(_translate("MainWindow", "Rx"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Channel"))
        self.rbn_A.setText(_translate("MainWindow", "A"))
        self.rbn_C.setText(_translate("MainWindow", "C"))
        self.rbn_B.setText(_translate("MainWindow", "B"))
        self.rbn_D.setText(_translate("MainWindow", "D"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
from pyqtgraph import PlotWidget
