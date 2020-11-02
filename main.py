# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append(r'.\ui')
import os


from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi(r"./ui/RuVue.ui", self)
        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        self.rbn_run.clicked.connect(self.run)

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)

    def run(self):
        str = ''
        if self.rbn_Tx.isChecked():
            str = 'You have choose Tx'
        elif self.rbn_Rx.isChecked():
            str = 'You have choose Rx'
        else:
            str = 'you should choose tx or rx firstly'

        if self.rbn_A.isChecked():
            str = str + ' Branch A'
        elif self.rbn_B.isChecked():
            str = str + ' Branch B'
        elif self.rbn_C.isChecked():
            str = str + ' Branch C'
        elif self.rbn_D.isChecked():
            str = str + ' Branch D'
        else:
            str = 'you should choose tx or rx firstly'

        self.label.setText(str)



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()

