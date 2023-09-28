#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:30:09 2023

@author: vboxuser
"""
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from myTable import MyTable 


class SQL_Engine():
#Отвечает за SQL запросы
    def __init__(self, tables):
        self.check_conect()
        self.add_tables(tables)
        
    def show_table(self, actual_table):
        #Вывод таблицы
        self.mod = QSqlQueryModel()
        self.mod.setQuery(actual_table.select)
        self.mod.lastError()
        return self.mod
    
    def main_show(self):
        #Показывает общий расходы
        mod = QSqlQueryModel()
        quer = "SELECT SUM(Покупки.price * Покупки.amout) AS Расход FROM Покупки"
        mod.setQuery(quer)
        return mod
    
    def check_conect(self):
        #Подключение к БД
        db = QSqlDatabase.addDatabase("QSQLITE");
        db.setHostName("localhost");
        db.setDatabaseName("hm_acc");
        db.setUserName("usert");
        db.setPassword("123");
        ok = db.open();
        
    def add_tables(self, tables):
    #Создаёт таблицы для приложения
        query = QSqlQuery()
        
      #  qcheck = "DROP TABLE Check"
       # if query.exec(qcheck) :
      #      return
        
        #Удаляет все таблицы (для дебага)
        self.drop_all_ts(query)
        
      
        for table in tables:
            if not (query.exec(self.crt_table(table.t_name, table.t_atr))):
                print("Error")
            
               
    def crt_table(self, name, atr):
        crt = ""
        match name:
            case "Расходы":
                crt = '''CREATE TABLE {0}
                (
                    {a[0]} INTEGER PRIMARY KEY,
                    {a[1]} DATETIME(100),
                    {a[2]} CHAR(100)
                )'''
            case "Покупки":
               crt = '''
               CREATE TABLE {0}
               (
                  {a[0]}  INTEGER REFERENCES Расходы(id_purchase),
                  {a[1]}  INTEGER,
                  {a[2]}  CHAR(100),
                  {a[3]}  INTEGER,
                  {a[4]}  INTEGER
               )
               '''
        crt = crt.format(name, a = atr)
        return crt
                    
    def drop_all_ts(self, query):
    #Удаляет все таблицы (для дебага)
        qcheck = "DROP TABLE Расходы"
        query.exec(qcheck)
        
        qcheck = "DROP TABLE Покупки"
        query.exec(qcheck)
        
        
    def val_mod(self, atr, value):
        print(value)
        if "date" in atr:
            val = "DATE('{0}')".format(value)
        elif "id_" in atr:
            val = value
        else:
            val = "'{0}'".format(value)
            
        return val
        
        
    def insert_into(self, actual_table, t_val):
        
        t_name = actual_table.t_name
        t_atr = actual_table.t_atr
        
        #Добавление записи
        str_in = "INSERT INTO {t} ({atr}) VALUES ({val})" 
        
        at = ""
        vl = ""
        
        #Подстановка значений по атрибутам
        for i in range(len(t_atr)):
            at += t_atr[i] + ", "
            
            mvl = self.val_mod(t_atr[i], t_val[i])
            vl += mvl + ", "
                          
        at = at[:-2]
        vl = vl[:-2]
               
        str_in = str_in.format(t = t_name, atr = at, val = vl)
        self.mod.setQuery(str_in)
        
        self.mod.setQuery(actual_table.select)
        return self.mod
        
    def get_max(self, t_name, id_atr):
        #Возвращает максимальный id
        query = QSqlQueryModel()
      
        qur = "SELECT max({0}.{1}) from {0}".format(t_name, id_atr)
        query.setQuery(qur)
   
        rec = query.record(0)
        val = rec.value(0)
                
        if (val == ""):
            return 1
        
        if (val == None):
            return 1
        
        return int(val) + 1
    
    

        
    
    def get_id_list(self):
    #Возвращает список родительских id
        query = QSqlQueryModel()
      
        qur = "SELECT id_purchase from {0}".format("Расходы")
        query.setQuery(qur)
        
        
        n = query.rowCount()
        id_list = []
        for i in range(0, n):
            rec = query.record(i)
            val = rec.value(0)
            print(val)
            id_list.append(str(val))
            pass
        return id_list
        

   
        
        
    def values_from(self, table_name, t_id, atr):
        query = QSqlQueryModel()
        qur = '''SELECT * FROM {tab}'''.format(tab = table_name)
                #WHERE {tab}.{a} = {id}'''.format(tab = table_name, a = atr,
                #id = t_id)
        query.setQuery(qur)
        
        lenq = query.columnCount()
        rec = query.record(t_id)
        
        vals = []
        for i in range(0,lenq):
            cal = rec.value(i)
            vals.append(cal)
            
        print(vals)
        return vals
     
    
    def deleate_id(self, id_val, actual_table):
        
        t_name = actual_table.t_name
        id_str = actual_table.t_atr
        query = QSqlQueryModel()
        qur = "DELETE from {table} WHERE {atr_id} = {val_id}".format(
                table = t_name, atr_id = id_str[0], val_id = id_val[0])
        
        print(qur)
        
        query.setQuery(qur)  
        
        quer = actual_table.select
        self.mod.setQuery(quer)
        
    def update_id(self, vals, actual_table, old_id):
        
         t_name = actual_table.t_name
         atr_str = actual_table.t_atr
         query = QSqlQueryModel()
       
         qur = "UPDATE {table} SET {set} WHERE {atr_id} = {val_id}".format(
                 table = t_name, atr_id = atr_str[0], val_id = old_id, 
                 set = self.formed_set(atr_str, vals))
         print(qur)
         query.setQuery(qur)
         quer = actual_table.select
         self.mod.setQuery(quer)
         
                 
    def formed_set(self, atr, val):
        alen = len(atr)
        print(alen)
        str_set = ""
        for i in range(alen):
            v_mod = self.val_mod( atr[i], val[i])
            temp = "{0} = {1}, ".format(atr[i], v_mod)
            str_set = str_set + temp
       
        return str_set[:-2]    
        
            