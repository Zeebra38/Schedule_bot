import sqlite3

from SubjestClass import Subject
from UserClass import User
from utils import weeknum

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
        for group in groups:
            cur.execute("insert into Groups(group_name) values (?)", [group])
        self.con.commit()

    def insert_subject(self, day: str, subject: Subject):
        cur = self.cur
        cur.execute("""insert into {} values (?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(day), subject.ready_to_insert_data)
        cur.execute("select * from {}".format(day))

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
        self.con.commit()

    def insert_user(self, user: User):
        cur = self.cur
        cur.execute("select group_id from Groups where group_name == (?)", [user.group_name])
        group_id = cur.fetchone()
        cur.execute("insert into Users(telegram_id, vk_id, Name, Surname, group_id)  values (?, ?, ?, ?, ?)",
                    user.ready_to_insert_data + list(group_id))
        self.con.commit()

    def update_user(self, user: User):
        cur = self.cur
        cur.execute("select group_id from Groups where group_name == (?)", [user.group_name])
        group_id = int(str(cur.fetchone()).replace('(', '').replace(')', '').replace(',', ''))
        cur.execute("""UPDATE Users
        set group_id = (?),
            Name = (?),
            Surname = (?)
        where telegram_id = (?)
        and vk_id = (?);""", [group_id, user.name, user.surname, user.telegram_id, user.vk_id])
        self.con.commit()

    def drop_tables(self):
        cur = self.cur
        for day in 'Monday Tuesday Friday Thursday Saturday Wednesday'.split():
            cur.execute("drop table if exists {};".format(day))
            cur.execute("""CREATE TABLE {} (
                "group_id"	INTEGER NOT NULL,
                "number"	INTEGER,
                "even"	INTEGER NOT NULL,
                "weeks"	TEXT NOT NULL,
                "Subject"	TEXT NOT NULL,
                "Instructor"	TEXT,
                "Type"	TEXT NOT NULL,
                "Class"	TEXT,
                "Link"	TEXT
            ); """.format(day))
        self.con.commit()

    def select_user(self, telegram_id='', vk_id=''):
        cur = self.cur
        cur.execute("""select * from Users
        where telegram_id == (?)
        and vk_id == (?)""", [telegram_id, vk_id])
        res = cur.fetchone()
        if res is not None:
            res = list(map(str, res))
            user = User(res[3], res[4], res[1], res[2], res[5])
            return user
        return None

    def select_day_by_user(self, day: str, user: User, week=weeknum()):
        if day == 'Sunday':
            return []
        cur = self.cur
        if user.group_id == '':
            cur.execute("select group_id from Groups where group_name == (?)", [user.group_name])
            group_id = int(str(cur.fetchone()).replace('(', '').replace(')', '').replace(',', ''))
        else:
            group_id = user.group_id
        vars = [f'{week} %', f'% {week}', f'% {week} %']
        cur.execute(
            """select D.number, D.weeks, D.Subject, D.Instructor, D.Type, D.Class
            from {day} D 
            left join Groups G on D.group_id = G.group_id
            where D.group_id = (?)
            and (D.weeks like '{var1}' 
            or D.weeks like '{var2}'
            or D.weeks like '{var3}')
            order by D.number""".format(
                day=day, var1=vars[0], var2=vars[1], var3=vars[2]), [group_id])
        res = cur.fetchall()
        return res

    def select_group_name(self, group_id: int):
        cur = self.cur
        cur.execute("""
        select group_name from Groups
        where group_id == (?)""", [group_id])
        res = str(cur.fetchone()).replace('(', '').replace(')', '').replace(',', '').replace('\'', '')
        return res

    def drop_users(self):
        cur = self.cur
        cur.execute("drop table if exists Users;")
        cur.execute("""
                create table Users
        (
            user_id     INTEGER
                primary key autoincrement
                unique,
            telegram_id INTEGER,
            vk_id       INTEGER,
            Name        TEXT,
            Surname     TEXT,
            group_id    INTEGER not null
        );""")
        self.con.commit()

    def check_group(self, group_name):
        self.cur.execute("select group_id from Groups where group_name == (?)", [group_name])
        res = self.cur.fetchone()
        return res
