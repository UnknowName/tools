#!/bin/env python
#coding:UTF8


import xlrd
import xlwt
from xlutils.copy import copy


def read(file_name):
    "读取Excel文件，并通过生成器，将每行返回。后续通过for迭代出来即可"
    excel = xlrd.open_workbook(file_name,encoding_override='utf8')
    for excel_sheet in excel.sheets():
        for i in range(excel_sheet.nrows):
            yield excel_sheet.row_values(i)

             
def write(file_name,iter_obj):
    "传入列表数据，将列表数据写入Excel文件"
    row = 0
    excel = xlwt.Workbook(encoding='utf8')
    excel_sheet = excel.add_sheet('sheet1')
    #如果是List类型，直接迭代写入文件中
    if isinstance(iter_obj, list):
        for col,data in enumerate(iter_obj):
            excel_sheet.write(row,col,data)     
        row += 1
    else:
        #这里处理不是List类型的。主要针对从数据库的cursor
        for lst in iter_obj:
            for col,data in enumerate(lst):
                excel_sheet.write(row,col,data)
            row += 1
    excel.save(file_name)
    return 200 

def append_row(file_name,lst_data): 
    "将lst_data数据追加进指定的Excel文件。追加行数据"
    excel = xlrd.open_workbook(file_name,encoding_override='utf8')
    #excel_sheet = excel.sheet_by_index(0)
    new_excel = copy(excel)
    new_sheet = new_excel.get_sheet(0)
    row = excel.sheet_by_index(0).nrows
    for col,data in enumerate(lst_data):
        new_sheet.write(row,col,data)
    row += 1
    new_excel.save(file_name)
    return 200
    
    
    
    