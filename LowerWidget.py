#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:51:48 2023

@author: vboxuser
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlQueryModel
from myTable import MyTable 

class LowerWidget(QWidget):
#Отвечает за виджет для ввода данных
    
    def __init__(self, table_v):
        super().__init__()
        self.lay = QGridLayout(self)
        self.tavlV = table_v
        
    
    def make_in_form(self, table_class, tst):
        #self.new_id = new_id
        #Виджет для вставки новоой записи )
        t_name = table_class.t_name
        t_atr = table_class.t_atr
        pen = table_class.t_pen_name
        
        #TEMP
        self.next_id = tst
        print(self.next_id, table_class.next_id )
        self.keys_for = table_class.keys_for
        
        self.change(t_atr, pen, t_name)
        self.butadd = QPushButton("Добавить запись")
        itms = self.lay.count()
        self.lay.addWidget(self.butadd, itms+1, 0, 1, 2)
    
    
    def make_up_form(self, table_class):
        #Генерация формы для обновления записи
        #self.new_id = new_id
        
        arg = table_class.t_atr
        tname = table_class.t_name
        pen = table_class.t_pen_name
        
        #TEMP
        self.next_id = table_class.next_id
        self.keys_for = table_class.keys_for
        
        self.change(arg, pen, tname)
        self.butupd = QPushButton("Обновить запись запись")   
        
        itms = self.lay.count()
        self.lay.addWidget(self.butupd, itms + 1, 0, 1, 2)
               
        self.butdel = QPushButton("Удалить запись")
        self.lay.addWidget(self.butdel, itms + 3, 0, 1, 2)

    
    
    
    
    
    def change(self, arg, pen, tname):
    #Перстраивает виджет под таблицу  
        self.table_now = tname
        self.clear_lay()
        self.widLE = []
        i = 0
        for i in range(len(arg)):
            lab = QLabel(pen[i])
            le = self.inp_widget_def(arg[i])
            self.lay.addWidget(lab, i, 0)
            self.lay.addWidget(le, i, 1)          
            self.widLE.append(le)
            i = i + 1
        
        
        
    def clear_lay(self):
    #Очистка лейаута
        while self.lay.count():
           c = self.lay.takeAt(0)
           c.widget().deleteLater()
           
    def get_values(self, atr):
    #Считывает данные из формы
        vals = []
        i = 0
        for w in self.widLE:
            if "date" in atr[i]:
                dt = w.date()
                str_date = dt.toString("yyyy-MM-dd")
                vals.append(str_date)
            elif "_fk" in atr[i]:
                s = w.currentText()
                vals.append(s)
            else:
                vals.append(w.text())
            i = i + 1
            
        return vals
    
    
    def inp_widget_def(self, atr):
    #Возвращает нужный индекс в зависимости от названия
        if 'date' in atr:
            de = QDateEdit(QDate.currentDate())
            return de
        elif '_fk' in atr:
            cb = QComboBox()
            cb.addItems(self.keys_for)
            return cb
        elif 'id' in atr:
            le = QLineEdit()
            le.setText(str(self.next_id))
            return le
        return QLineEdit()
    
    def set_values(self, value, atr):
    #Считывает данные из формы
        i = 0
        for w in self.widLE:
            if "date" in atr[i]:
                w.setDate(QDate.fromString(str(value[i]), "yyyy-MM-dd"))
            elif "_fk" in atr[i]:
                le = QLineEdit(str(value[i]))
                w.setLineEdit(le)
                pass
            else:
                w.setText(str(value[i]))
            i = i + 1
     
    
    
            
        
        
        