#-*- encoding: utf-8 -*-
import xlrd
import readEmail
import os

BASE_DIR= os.path.dirname(os.path.realpath(__file__))
FILE_DIR = BASE_DIR + '/file'

def getexcel():
    file =FILE_DIR + '/'+ readEmail.getemail()
    result = []
    data = xlrd.open_workbook(file)
    if len(data.sheets())>0:
        for i in data.sheets():
            result.append(int(i._cell_values[i.nrows-1][i.ncols-1]))
    return result

if __name__ == "__main__":
    print getexcel()