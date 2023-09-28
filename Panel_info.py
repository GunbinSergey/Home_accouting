
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 16:47:13 2023

@author: vboxuser
"""

from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from SQLEngine import SQL_Engine
from LowerWidget import LowerWidget
from MyTableWidget import TableWidget

class Panel_info(QWidget):
    #Пустые виджеты для настроек при необходимости
    #uper_wid
    #lower_wid
    
    def __init__(self):
        super().__init__()
        self.ensql = SQL_Engine()
        
        table_View = TableWidget()
        
        
        layb = QVBoxLayout(self)   
        self.uper_wid = QWidget()
        self.table.clicked.connect(self.s_update_delete)
        
        self.lower_wid = LowerWidget(self.table_View)
        
        layb.addWidget(self.uper_wid)
        layb.addWidget(self.table)
        layb.addWidget(self.lower_wid)
        
        
        
        
    
        
   