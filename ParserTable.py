import openpyxl
from openpyxl.utils import get_column_letter
import re
from SubjestClass import *
from DataBase import Schedule
from utils import translate_weekday
schedule = Schedule()

def ParserTable(name_table):
    name_table = "schedules\КБиСП 2 курс 2 сем-Д (3).xlsx"  # потом может удалить

    table = openpyxl.open(name_table, read_only=True)

    sheet = table.active

    search_text = "БПБО-02-19"
    search_text = search_text.lower()

    wb = openpyxl.load_workbook(name_table)
    sheets_list = wb.sheetnames
    sheet_active = wb[sheets_list[0]]
    row_max = 2
    column_max = sheet_active.max_column
    # print(column_max, ' ', row_max) # проверка количества строк и столбцов
    row_min = 2
    column_min = 1
    while column_min <= column_max:
        row_min_min = row_min
        row_max_max = row_max

        row_min_min = str(row_min_min)

        word_column = get_column_letter(column_min)
        word_column = str(word_column)
        word_cell = word_column + row_min_min

        data_from_cell = sheet_active[word_cell].value
        data_from_cell = str(data_from_cell)
        # print(data_from_cell)
        regular = search_text
        if len(data_from_cell) > 9:
            if data_from_cell[4] == '-' and data_from_cell[7] == '-':
               # print('Нашли в ячейке:', column_min, " ", row_min_min)
                # print(data_from_cell)
               # print(sheet[2][int(column_min) - 1].value[0:10])
                pass

        if 'БПБО-02-19' in data_from_cell:
            #print('Бпбо-02-19 находится в ячейке:', column_min, " ", row_min_min)
            #print(get_column_letter(column_min), get_column_letter(column_min+4))
            cells = sheet[get_column_letter(column_min)+'4':get_column_letter(column_min+4)+'75']
            chetnost = 1
            NomerPar = 2
            DenNedeli = 4
            subjets = []
            for item, vid_zanyatiy, FIO, nomer, ssilka in cells:

                if NomerPar == 14:
                    NomerPar -= 12
                    DenNedeli += 12


                if item.value != None and "\n" in item.value:
                    ForMultiSubject = MultiSubject(data_from_cell, NomerPar, chetnost % 2, item.value, vid_zanyatiy.value,
                                                    FIO.value, nomer.value, ssilka.value)
                    schedule.insert_subjects(translate_weekday(sheet[DenNedeli][0].value), ForMultiSubject.subjects)#инглишменский день

                elif item.value != None:
                    ForSubject = Subject(data_from_cell, NomerPar, chetnost % 2, item.value, vid_zanyatiy.value,
                                                    FIO.value, nomer.value, ssilka.value)
                    subjets.append(ForSubject)

                print(item.value, vid_zanyatiy.value, FIO.value, nomer.value,
                       ssilka.value, NomerPar//2, sheet[DenNedeli][0].value, chetnost % 2)
                chetnost += 1
                NomerPar += 1
            schedule.insert_subjects(translate_weekday(sheet[DenNedeli][0].value), subjets)
            break

        row_min_min = int(row_min_min)

        column_min = column_min + 1

    print(sheet[5][0].value) #row_min_min -1
    #return ForMultiSubject

def GroupsList():
    name_table = "schedules\КБиСП 2 курс 2 сем-Д (3).xlsx"  # потом может удалить

    table = openpyxl.open(name_table, read_only=True)

    sheet = table.active

    search_text = "БПБО-02-19"
    search_text = search_text.lower()

    wb = openpyxl.load_workbook(name_table)
    sheets_list = wb.sheetnames
    sheet_active = wb[sheets_list[0]]
    row_max = 2
    column_max = sheet_active.max_column
    # print(column_max, ' ', row_max) # проверка количества строк и столбцов
    row_min = 2
    column_min = 1
    GroupList = []
    while column_min <= column_max:
        row_min_min = row_min
        row_max_max = row_max

        row_min_min = str(row_min_min)

        word_column = get_column_letter(column_min)
        word_column = str(word_column)
        word_cell = word_column + row_min_min

        data_from_cell = sheet_active[word_cell].value
        data_from_cell = str(data_from_cell)
        # print(data_from_cell)
        regular = search_text
        if len(data_from_cell) > 9:
            if data_from_cell[4] == '-' and data_from_cell[7] == '-':
                #print('Нашли в ячейке:', column_min, " ", row_min_min)
                #print(data_from_cell)
                #print(sheet[2][int(column_min) - 1].value[0:10])
                GroupList += [sheet[2][int(column_min) - 1].value[0:10]]
        row_min_min = int(row_min_min)

        column_min = column_min + 1
    print(GroupList)

#GroupsList()
ParserTable(1)
