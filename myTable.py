#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:14:03 2023

@author: vboxuser
"""

class MyTable():
    def __init__(self, name, atr, pen_name, sel = ""):
        if sel == "":
            self.select = self.select_as(name, atr, pen_name)
        else:
            self.select = sel;
        
        self.t_name = name
        self.t_atr = atr
        self.t_pen_name = pen_name
        
        self.next_id = "0"
        self.keys_for = []
        
        
        
    def select_as(self, name, atrs, pen_name):
    #Возвращает с псевданимами
    
        t_name = name
        art = atrs
        pen = pen_name
        sel = ""
        
        base = "SELECT {0} from {1}"
        for i in range(len(art)):
            sel = sel + "{a[" + str(i) +"]} AS {p[" + str(i) +"]}, "
        sel = sel[:-2]
        sel = sel.format(a = art, p = pen)
        #sel = "*"
        quer = base.format(sel, t_name)
        print(quer)
        return quer