import openpyxl
from openpyxl.utils import get_column_letter
import re
from SubjestClass import *
from DataBase import Schedule

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
               # print(sheet[2][int(column_min) - 1].value[0:10])  # Список групп
                pass

        if 'БПБО-02-19' in data_from_cell:
            print('Бпбо-02-19 находится в ячейке:', column_min, " ", row_min_min)
            #for row in sheet.iter_rows(min_row=int(row_min_min) + 1, max_row=75, min_col=int(column_min),
                 #                      max_col=int(column_min) + 4):
               # for cell in row:
               #     print(cell.value, end=' ')
               # print()
            cells = sheet['HW20':'IA26']

            for item, vid_zanyatiy, FIO, nomer, ssilka in cells:
                if item.value != None and "\n" in item.value:
                    nomer1 = str(nomer.value)
                    nomer1 += "\n пошел нахуй этот вуз ебанный"
                    vid_z = str(vid_zanyatiy.value)
                    vid_z += "\n пошел нахуй этот вуз ебанный"
                    ForMultiSubject = MultiSubject(data_from_cell, 1, 0, item.value, vid_z,
                                                   FIO.value, nomer1, "ssilka\nvalue")  # todo 1 = номер предмета
                    schedule.insert_subjects("Monday", ForMultiSubject.subjects)#инглишменский день
                print(item.value, vid_zanyatiy.value, FIO.value, nomer.value,
                      ssilka.value)  # todo День недели. Создать класс и вызвать функцию

            break

        row_min_min = int(row_min_min)

        column_min = column_min + 1

    # print(sheet[2][230].value) #row_min_min -1
    return ForMultiSubject


ParserTable(1)
