import sqlite3

from SubjestClass import Subject
from UserClass import User


class Schedule:

    def __init__(self, path='private/rasp.db'):
        """Создание соединения с БД. path - путь к БД. con-соединение, cur-курсор"""
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def insert_groups(self, groups: list[str]):
        cur = self.cur
        cur.execute("drop table if exists Groups;")
        cur.execute("""CREATE TABLE "Groups" (
        "group_id" INTEGER NOT NULL UNIQUE,
        "group_name"	TEXT NOT NULL UNIQUE,
        PRIMARY KEY("group_id" AUTOINCREMENT));""")
        # cur.execute("insert into Groups(group_name) values (?)", (groups, ))
        for group in groups:
            cur.execute("insert into Groups(group_name) values (?)", [group])
        # cur.executemany("insert into Groups(group_name) values (?)", groups) #todo НЕ РАБОТЕТ
        # self.con.commit()
        cur.execute("select * from Groups")
        print(cur.fetchall())
        self.con.commit()

    def insert_subject(self, day: str, subject: Subject):
        cur = self.cur
        cur.execute("""insert into {} values (?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(day), subject.ready_to_insert_data)
        cur.execute("select * from {}".format(day))
        all_result = cur.fetchall()
        print(all_result)

    def insert_subjects(self, day: str, subjects: [Subject]):
        cur = self.cur
        group_ids = []
        for group_name in [[subj.group_name] for subj in subjects]:
            cur.execute("select group_id from Groups where group_name == (?)", group_name)
            group_ids.append(cur.fetchone())
        data = []
        for i in range(len(group_ids)):
            data.append(list(group_ids[i]) + subjects[i].ready_to_insert_data)
        cur.executemany("""insert into {} values (?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(day),
                        data)
        cur.execute("select * from {}".format(day))
        all_result = cur.fetchall()
        print(all_result)
        self.con.commit()

    def insert_user(self, user: User):
        cur = self.cur
        cur.execute("select group_id from Groups where group_name == (?)", [user.group_name])
        group_id = cur.fetchone()
        cur.execute("insert into Users(telegram_id, vk_id, Name, Surname, group_id)  values (?, ?, ?, ?, ?)",
                    user.ready_to_insert_data + list(group_id))
        cur.execute("select * from Users")
        print(cur.fetchall())

    def select_day_by_user(self, day: str, user: User):
        cur = self.cur
        cur.execute("select group_id from Groups where group_name == (?)", [user.group_name])
        group_id = str(cur.fetchone())
        cur.execute(
            """select G.group_name, D.number, D.even, D.weeks, D.Subject, D.Instructor, D.Type, D.Class, D.Link 
            from {} D 
            left join Groups G on D.group_id = G.group_id
            where D.group_id = (?)
            order by D.number""".format(
                day), [group_id])
        print(cur.fetchall())