import re


class Subject:
    """
    group_name - название группы str, number - порядкой номер int, even - четность (1/0) int, 
    subj - предмет вместе с номерами недель str, _type - тип str,
    instructor - преподаватель str, _class  - аудитория str, link - ссылка str
    """

    def __init__(self, group_name, number, even, subj, _type, instructor, _class, link, exam=0):
        self.group_name = group_name
        self.number = number
        self.even = even
        self._type = _type if _type is not None else ''
        self.instructor = instructor if instructor is not None else ''
        self._class = str(_class) if _class is not None else ''
        self.link = link if link is not None else ''
        self.name, self.weeks = self.set_up_subject(subj, even)
        self.exam = exam
        self.ready_to_insert_data = [self.number, self.even, " ".join(self.weeks), self.name, self._type,
                                     self.instructor, self._class, self.link, self.exam]

    def set_up_subject(self, subj, even):
        subj = subj.replace('.', ',').replace(',', ' ')
        pattern = r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?"
        odd_weeks = '1 3 5 7 9 11 13 15'.split()
        even_weeks = '2 4 6 8 10 12 14 16'.split()
        started_weeks = re.findall(pattern, subj)
        if len(started_weeks) == 0:
            if even:
                weeks = even_weeks

            else:
                weeks = odd_weeks

            name = subj
        else:
            if re.match(r'^кр', subj):
                if even:
                    set2 = set(started_weeks)
                    weeks = [o for o in even_weeks if o not in set2]
                else:
                    set2 = set(started_weeks)
                    weeks = [o for o in odd_weeks if o not in set2]
            else:
                weeks = started_weeks
            name = subj[subj.find('н') + 1:].strip()

        self.weeks = weeks
        if len(self.weeks) >= 2:
            if int(self.weeks[-1]) < int(self.weeks[-2]):
                self.weeks.pop(-1)
        return name, weeks

    def __str__(self):
        return self.ready_to_insert_data


class MultiSubject:
    """Используется, когда в строке несколько различных предметов. Передаются все параметры, также, как и в обычном
    классе Subject. Будет происходить split по '\n'. Чтобы обращаться к предметам внутри есть свойство subjects,
    возвращающее массив Subject"""

    def __init__(self, group_name, number, even, subj, _type, instructor, _class, link, exam=0):
        def increase_arguments(a, b):
            if len(a) < len(b):
                for _ in range(len(b) - len(a)):
                    a.append(a[0])
            return a
        if _class is None:
            _class = ''
        _class = str(_class)
        if link is None:
            link = ''
        if instructor is None:
            instructor = ''
        subjs = subj.split('\n')
        types = _type.split('\n')
        instructors = instructor.split('\n')
        classes = _class.split('\n')
        links = link.split('\n')
        types = increase_arguments(types, subjs)
        instructors = increase_arguments(instructors, subjs)
        classes = increase_arguments(classes, subjs)
        links = increase_arguments(links, subjs)
        self.subjects = []
        for subj, _type, instructor, _class, link in zip(subjs, types, instructors, classes, links):
            self.subjects.append(Subject(group_name, number, even, subj, _type, instructor, _class, link, exam))
