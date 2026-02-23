# models.py
from datetime import datetime
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            # Validate that phone number is exactly 10 digits
            raise ValueError("Phone number must be exactly 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # очікуємо формат DD.MM.YYYY і перевіряємо формат дати
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record: # Клас Record представляє окремий контакт у адресній книзі
    def __init__(self, name: str): 
        self.name = Name(name) # обов'язково поле для зберігання об'єкта Name
        self.phones = [] # список об'єктів Phone, спочатку порожній список
        self.birthday = None # необов'язкове поле для зберігання об'єкта Birthday, спочатку None

    def add_birthday(self, birthday_str: str): # додає дату народження до контакту
        self.birthday = Birthday(birthday_str) 

    def add_phone(self, phone: str): # додає новий номер телефону до контакту
        if any(p.value == phone for p in self.phones):
            return False
        self.phones.append(Phone(phone))
        return True

    def remove_phone(self, phone: str):  # видаляє номер телефону з контакту
        matches = [p for p in self.phones if p.value == phone]
        if not matches:
            return False  # номер не знайдено
        self.phones.remove(matches[0]) # видаляємо перший знайдений номер
        return True


    def find_phone(self, phone: str): # шукає номер телефону в контакті
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None
        
    def edit_phone(self, old_phone: str, new_phone: str): # Змінює існуючий номер телефону на новий
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError("Old phone number not found")
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    