import openpyxl
from openpyxl.utils import get_column_letter
import re
from SubjestClass import *
from DataBase import Schedule
from utils import translate_weekday
import UserClass
from threading import *
from time import time, sleep
import os

GroupList = []

subjects = {}
multisubjects = {}


def Parser_Table(name_table):
    # name_table = "schedules\КБиСП 2 курс 2 сем-Д (3).xlsx"  # потом может удалить
    start = time()

    group_list_local = []
    table = openpyxl.open(name_table, read_only=True)

    sheet = table.active

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
        if len(data_from_cell) > 9:
            if data_from_cell[4] == '-' and data_from_cell[7] == '-' and data_from_cell not in group_list_local:
                # print('Нашли в ячейке:', column_min, " ", row_min_min)
                # print(data_from_cell)
                # print(sheet[2][int(column_min) - 1].value[0:10])
                # pass
                group_list_local.append(data_from_cell)
                # if 'БПБО-02-19' in data_from_cell:
                # print('Бпбо-02-19 находится в ячейке:', column_min, " ", row_min_min)
                # print(get_column_letter(column_min), get_column_letter(column_min+4))
                cells = sheet[get_column_letter(column_min) + '4':get_column_letter(column_min + 4) + '75']
                chetnost = 0
                NomerPar = 2
                DenNedeli = 4
                subjets = []
                for item, vid_zanyatiy, FIO, nomer, ssilka in cells:

                    if NomerPar == 14:
                        NomerPar -= 12
                        # schedule.insert_subjects(translate_weekday(sheet[DenNedeli][0].value), subjets)
                        subjets.clear()
                        DenNedeli += 12

                    if item.value != None and "\n" in item.value:
                        try:
                            ForMultiSubject = MultiSubject(data_from_cell[:10], NomerPar // 2, chetnost % 2, item.value,
                                                       vid_zanyatiy.value,
                                                       FIO.value, nomer.value, ssilka.value)
                        except Exception as e:
                            print(str(e))
                            a = 1/(1-1)
                        global multisubjects
                        multisubjects[ForMultiSubject] = translate_weekday(sheet[DenNedeli][0].value)
                        # schedule.insert_subjects(translate_weekday(sheet[DenNedeli][0].value), ForMultiSubject.subjects)#инглишменский день

                    elif item.value != None:
                        ForSubject = Subject(data_from_cell[:10], NomerPar // 2, chetnost % 2, item.value,
                                             vid_zanyatiy.value,
                                             FIO.value, nomer.value, ssilka.value)
                        global subjects
                        subjects[ForSubject] = translate_weekday(sheet[DenNedeli][0].value)
                        # subjets.append(ForSubject)

                    # print(item.value, vid_zanyatiy.value, FIO.value, nomer.value,
                    #        ssilka.value, NomerPar//2, sheet[DenNedeli][0].value, chetnost % 2)
                    chetnost += 1
                    NomerPar += 1

        row_min_min = int(row_min_min)

        column_min = column_min + 1
    print(time()-start, name_table)
    # print(sheet[5][0].value) #row_min_min -1
    #barrier.wait()
    # return ForMultiSubject


def Groups_List(name_table, barrier):
   # name_table = "schedules\КБиСП 2 курс 2 сем-Д (3).xlsx"  # потом может удалить

    table = openpyxl.open(name_table, read_only=True)

    sheet = table.active
    wb = openpyxl.load_workbook(name_table)
    sheets_list = wb.sheetnames
    sheet_active = wb[sheets_list[0]]
    row_max = 2
    column_max = sheet_active.max_column
    # print(column_max, ' ', row_max) # проверка количества строк и столбцов
    row_min = 2
    column_min = 1
    global GroupList

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
        if len(data_from_cell) > 9:
            if data_from_cell[4] == '-' and data_from_cell[7] == '-' and data_from_cell[:10] not in GroupList:
                #print('Нашли в ячейке:', column_min, " ", row_min_min)
                #print(data_from_cell)
                #print(sheet[2][int(column_min) - 1].value[0:10])

                GroupList.append(data_from_cell[0:10])
        row_min_min = int(row_min_min)

        column_min = column_min + 1
    # print(GroupList)
    # return GroupList
    barrier.wait()


def SchedulePars():
    schedule = Schedule()
    #schedule.drop_tables()
    os.chdir('./schedules')  # переход на работу с другой директорией
    # print(os.listdir()) # весь список всего
    global GroupList
    GroupList = []
    barrier = Barrier(len(os.listdir()) + 1)
    start = time()
    for NameTable12 in os.listdir():  # цикл для работы с списком ссего
        GL = Thread(target=Groups_List, args=(NameTable12, barrier,))
        GL.start()
    barrier.wait()
    schedule.insert_groups(GroupList)

    # GL = Thread(target = GroupsList, args=(NameTable12,))
    # GL.start()
    # GL.join()

    global subjects, multisubjects
    subjects.clear()
    multisubjects.clear()
    #barrier = Barrier(len(os.listdir()) + 1)
    for NameTable1 in os.listdir():  # цикл для работы с списком всего
        Parser_Table(NameTable1)



    print(time() - start)
    for key, value in multisubjects.items():
        schedule.insert_subjects(value, key.subjects)
    subjects_grouped_by_weekday = {key: [] for key in 'Monday Tuesday Wednesday Thursday Friday Saturday'.split()}
    for key, value in subjects.items():
        subjects_grouped_by_weekday[value].append(key)
    for key, value in subjects_grouped_by_weekday.items():
        schedule.insert_subjects(key, value)
    schedule.con.close()
SchedulePars()
# schedule.insert_groups(GroupsList())