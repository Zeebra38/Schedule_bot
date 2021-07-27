import sqlite3


class Schedule():

    def __init__(self, path='private/rasp.db'):
        """Создание соединения с БД. path - путь к БД. con-соединение, cur-курсор"""
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def groups_change(self, groups: list[str]):
        cur = self.cur
        cur.execute("drop table if exists Groups;")
        cur.execute("""CREATE TABLE "Groups" (
        "group_id" INTEGER NOT NULL UNIQUE,
        "group_name"	TEXT NOT NULL UNIQUE,
        PRIMARY KEY("group_id" AUTOINCREMENT));""")
        cur.executemany("insert into Groups(group_name) values (?)", [groups])


schedule = Schedule()
schedule.groups_change(['БПБО-02-19', "ЭЭЭЭ-03-20"])
