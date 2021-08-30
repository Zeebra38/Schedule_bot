class User:
    def __init__(self, name: str, surname="", telegram_id="", vk_id="", group_id="", group_name=""):
        self.name = name
        self.surname = surname
        self.telegram_id = telegram_id
        self.vk_id = vk_id
        self.group_name = group_name
        self.group_id = group_id
        self.ready_to_insert_data = [telegram_id, vk_id, name, surname]

    def __str__(self):
        return f'{self.name} {self.surname}, tg_id = {self.telegram_id}, vk_id = {self.vk_id}, ' \
               f'group_name = {self.group_name}, group_id = {self.group_id}'
