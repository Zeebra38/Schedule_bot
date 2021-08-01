import re


class Subject:
    """
    group_name - название группы str, number - порядкой номер int, even - четность (1/0) int, 
    subj - предмет вместе с номерами недель str, _type - тип str,
    instructor - преподаватель str, _class  - аудитория str, link - ссылка str
    """

    def __init__(self, group_name, number, even, subj, _type, instructor, _class, link):
        self.group_name = group_name
        self.number = number
        self.even = even
        self._type = _type
        self.instructor = instructor
        self._class = _class
        self.link = link
        self.name, self.weeks = self.set_up_subject(subj, even)

    def set_up_subject(self, subj, even):
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
        return name, weeks


class MultiSubject:
    """Используется, когда в строке несколько различных предметов"""

    def __init__(self):
        pass
