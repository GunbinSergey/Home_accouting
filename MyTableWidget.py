#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:06:21 2023

@author: vboxuser
"""

from PyQt5.QtWidgets import *
from myTable import MyTable
from SQLEngine import SQL_Engine
from LowerWidget import LowerWidget

class TableWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.tables = {}
        table_list = []
        self.table_view = QTableView()
       
        
        #Добавление таблиц
        tab_name = "Расходы"
        tab_atr = ["id_purchase", "sh_date", "item"]
        tab_pn = ["[id закупки]", "[Дата покупки]", "Маганзин", "Цена"]        
        
        sel = '''SELECT Расходы.{a[0]} AS {p[0]}, Расходы.{a[1]} AS {p[1]}, 
        Расходы.{a[2]} AS {p[2]}, SUM(Покупки.price * Покупки.amout) AS {p[3]} FROM Расходы
        INNER JOIN Покупки 
        ON Расходы.id_purchase == Покупки.id_purchase_fk
        GROUP BY Расходы.id_purchase, Расходы.sh_date, Расходы.item'''.format(a = tab_atr, p = tab_pn)

        temp_table = MyTable(tab_name, tab_atr, tab_pn, sel)        
        
        
        self.tables[tab_name] = temp_table
        table_list.append(temp_table)
        
        tab_name = "Покупки"
        #tab_atr = ["id_sele" , "id_purchase_fk", "item", "amout", "price"]
        #tab_pn = ["[id закупки]", "[id звкупки]", "Покупка", "[Кол-во]", "Цена"]
        
        tab_atr = [ "t_id", "id_purchase_fk", "item", "amout", "price"]
        tab_pn = [ "[id покупки]", "[id закупки]", "Покупка", "[Кол-во]", "Цена"]
        
        
        temp_table = MyTable(tab_name, tab_atr, tab_pn)    
        self.tables[tab_name] = temp_table
        table_list.append(temp_table)
       
        self.ensql = SQL_Engine(table_list)
        
        layb = QVBoxLayout(self)   
        self.uper_wid = QWidget()
        self.table = QTableView()
       
        self.lower_wid = LowerWidget(self)
        
        layb.addWidget(self.uper_wid)
        layb.addWidget(self.table_view)
        layb.addWidget(self.lower_wid)
        
        self.table_view.clicked.connect(self.s_update_delete)
           
        
    def con_show(self):
        #Функция-костыль для вывода таблиц
        sender = self.sender()
        tname = sender.text()
        self.actual_table = self.tables.get(tname)
        self.show_table(self.actual_table)      
               
       
    def show_table(self, show_table):
        name = self.actual_table.t_name
        self.table_view.setModel(self.ensql.show_table(self.actual_table))
      
        
        if name == "Расходы":
            self.actual_table.new_id = self.ensql.get_max(name, show_table.t_atr[0])
            
        elif name ==  "Покупки":
            self.actual_table.new_id = self.ensql.get_max(name, show_table.t_atr[0])
            self.actual_table.keys_for = self.ensql.get_id_list()
                   
        self.lower_wid.make_in_form(self.actual_table, self.actual_table.new_id )
        
        but = self.lower_wid.butadd
        but.clicked.connect(self.con_insert)
        
        
    def con_insert(self):
        value = self.lower_wid.get_values(self.actual_table.t_atr)
        
        self.table_view.setModel(
            self.ensql.insert_into(self.actual_table, value)
        )
        self.show_table(self.actual_table)
        
        
        
    def main_show(self):
        #self.table_view.setModel(self.ensql.main_show())
        self.table_view.setModel(self.ensql.main_show())
        self.lower_wid.clear_lay()
        
            
    def s_update_delete(self, index):
        self.wid = LowerWidget(self.table_view)
        

        self.wid.make_up_form(self.actual_table)
        self.row = index.row()
        
        self.vals = self.ensql.values_from(self.actual_table.t_name, self.row, 
                                           self.actual_table.t_atr)
        self.wid.set_values(self.vals,   self.actual_table.t_atr)
        
        #Для Апдейт
        self.old_id = self.vals[0]
        self.wid.butupd.clicked.connect(self.con_update)
        self.wid.butdel.clicked.connect(self.con_deleate)      
        self.wid.show()
        
        
    def con_deleate(self):
        self.ensql.deleate_id(self.vals, self.actual_table)
        pass

    def con_update(self):
        atr = self.actual_table.t_atr
        vals = self.wid.get_values(atr)
        self.ensql.update_id(vals, self.actual_table, self.old_id)
        pass