class User:
    def __init__(self, name, surname="", telegram_id="", vk_id="", group_name=""):
        self.name = name
        self.surname = surname
        self.telegram_id = telegram_id
        self.vk_id = vk_id
        self.group_name = group_name
        self.ready_to_insert_data = [telegram_id, vk_id, name, surname]
