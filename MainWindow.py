#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:50:04 2023

@author: vboxuser
"""
import sys
from PyQt5.QtWidgets import *
from Panel_info import *


class MainWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
          
        self.setCentralWidget(self.cent_wid())

    def cent_wid(self):
    #Наполнение стандартного вывода
        wid = QWidget()
        lay_h = QHBoxLayout(wid)
        
        tst = QLabel("tst")
        self.pan = TableWidget()
        
        lay_h.addWidget(self.seting_panel())       
        lay_h.addWidget(self.pan)
        
        lay_h.setStretch(0, 20)
        lay_h.setStretch(1, 80)
        return wid
        
    def seting_panel(self):
    #Боковая панель с настойкой вывода
        wid = QWidget()
        
        lay_v = QVBoxLayout(wid)
        
        #lab_dat1 = QLabel("Начало периода")
        #lab_dat2 = QLabel("Конец периода")
        
        #self.dat_pos1 = QCalendarWidget()
        #self.dat_pos2 = QCalendarWidget()
        
        but_main = QPushButton("Главная")
        but_credit = QPushButton("Расходы")
        but_purchase = QPushButton("Покупки")
        
        #Назначение действий при нажатии
        but_main.clicked.connect(self.pan.main_show)
        but_credit.clicked.connect(self.pan.con_show)
        but_purchase.clicked.connect(self.pan.con_show)
        
        #lay_v.addWidget(lab_dat1)
        #lay_v.addWidget(self.dat_pos1)
        #lay_v.addWidget(lab_dat2)
        #lay_v.addWidget(self.dat_pos2)
        lay_v.addWidget(but_main)
        lay_v.addWidget(but_credit)
        lay_v.addWidget(but_purchase)
        
        
        
        return wid


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main = MainWidget()
    main.show()
    
    sys.exit(app.exec_())