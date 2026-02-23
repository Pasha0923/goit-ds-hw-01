# address_book.py
from collections import UserDict
from datetime import datetime, date, timedelta
from models import Record

class AddressBook(UserDict): 
    ''' Словник контактів (клас AddressBook відповідає за збереження та управління колекцією контактів) '''
    def add_record(self, record:Record ): # додає новий запис до адресної книги
        self.data[record.name.value] = record

    def find(self, name: str):  # шукає контакт за ім'ям і повертає відповідний запис або None, якщо контакт не знайдено
        return self.data.get(name)
    
   # видаляє контакт за ім'ям
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    # Виводить всі записи в адресній книзі у вигляді рядка
    def __str__(self):
        if not self.data:
            return "AddressBook is empty"
        return "\n".join(str(record) for record in self.data.values())
    
    
    def date_to_string(self,date): # перетворює об'єкт дати(date) на рядок у форматі "DD.MM.YYYY"
        return date.strftime("%d.%m.%Y")

    def find_next_weekday(self, start_date, weekday): # знаходить наступну дату певного дня тижня після заданої дати
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday): # Переносить день народження на понеділок, якщо він випадає на вихідні
        # 0 - понеділок, 6 - неділя
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0) 
        return birthday

    def get_upcoming_birthdays(self, days=7): # отримує список користувачів з днями народження, які відзначаються протягом наступних 'days' днів
        """
            Повертає список словників {"name": name, "birthday": "DD.MM.YYYY"}
            для тих контактів, у яких день народження в найближчі `days` днів
            (включая сьогоднішній).Якщо дата випадає на вихідні, переносимо на понеділок.
        """
        upcoming_birthdays = [] 
        today = date.today() # Поточна дата

        for record in self.data.values(): 
            if record.birthday is None: 
                continue 

            try: # Перевіряємо коректність формату дати народження
                datetime_obj = datetime.strptime(record.birthday.value, "%d.%m.%Y").date() 
            except ValueError: 
                continue  

            
            birthday_this_year = datetime_obj.replace(year=today.year) # Замінюємо рік народження на поточний рік
            if birthday_this_year < today: 
               birthday_this_year = birthday_this_year.replace(year=today.year + 1) 

           # Перевіряємо, чи день народження в межах наступних 'days' днів
            if 0 <= (birthday_this_year - today).days <= days: 
                congratulation_date =  self.adjust_for_weekend(birthday_this_year) 
                upcoming_birthdays.append({"name": record.name.value, 
                                           "birthday": self.date_to_string(congratulation_date)})        
        return upcoming_birthdays if upcoming_birthdays else "No upcoming birthdays in the next seven days"
        #  повертаємо список з днями народження в найближчі days' днів або повідомлення, якщо немає майбутніх днів народжень



    