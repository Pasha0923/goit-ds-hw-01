# handlers.py
from address_book import AddressBook
from models import Record, Phone
from functools import wraps

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError) as e:
            msg = str(e).lower() 
            if "unpack" in msg or "too many values" in msg or "not enough" in msg: 
                return "❌ Please provide the correct number of arguments"
            return f"❌ {e}"
        except KeyError:
            return "❌ This contact does not exist"
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                return "❌ Contact not found"
            return f"An unexpected attribute error occurred: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return inner
    
def parse_input(user_input: str) -> tuple:
    """
    Parses user input into command and arguments.
    Args:
        user_input (str): input string from user.
    Returns:
        tuple: (command, args)
    """
    parts = user_input.strip().split()
    if not parts:
        return '', []
    return parts[0].lower(), parts[1:]


@input_error
def add_contact(args, book: AddressBook):
    # args: ["John", "1234567890"]
    name, phone, *_ = args  
    record = book.find(name)  
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook): # Змінює номер телефону контакту за ім'ям
    # args: ["John", "1234567890", "0987654321"]
    name, old_phone, new_phone = args
    record = book.find(name)
    old_phone_obj = Phone(old_phone) 
    new_phone_obj = Phone(new_phone)  
    record.edit_phone(old_phone_obj.value, new_phone_obj.value) 
    return "Phone number updated"


@input_error
def show_phone(args, book: AddressBook): # Показує всі номери телефону контакту за ім'ям
    # args: ["John"]
    name, *_ = args
    record = book.find(name)
    if not record.phones:
        return "No phone numbers found for this contact"
    phones = ', '.join(phone.value for phone in record.phones)
    return f"Phone numbers for {name}: {phones}"

@input_error
def show_all(book: AddressBook): # Показує всі контакти в адресній книзі name phoone birthday(якщо вказано)
    if not book.data:
        return "AddressBook is empty."
    result = []
    for record in book.data.values():
        phones = ', '.join(phone.value for phone in record.phones) if record.phones else "No phone numbers"
        if record.birthday: 
            result.append(f"{record.name.value}: {phones} | Birthday: {record.birthday.value}")
        else:
            result.append(f"{record.name.value}: {phones} | No birthday")
    return "\n".join(result)

@input_error
def delete_phone(args, book: AddressBook): # Видаляє номер телефону контакту за ім'ям
    # args: ["John", "1234567890"]
    name, phone_str = args
    record = book.find(name)
    phone = Phone(phone_str)  
    result = record.remove_phone(phone.value)
    if result:
        return f"Phone {phone.value} removed for {name}"
    else:
        return f"❌ Phone number '{phone.value}' not found for contact {name}"

@input_error
def add_birthday(args, book: AddressBook): # Додає день народження контакту за ім'ям
    # args: ["John", "01.01.1990"]   
    name, birthday_str = args
    record = book.find(name)
    record.add_birthday(birthday_str)
    return f"Birthday for {name} to {birthday_str}"

@input_error
def show_birthday(args, book: AddressBook): # Показує день народження контакту за ім'ям
    # args: ["John"]
    name, *_ = args
    record = book.find(name)
    if not record.birthday:
        return f"No birthday for {name}"
    return f"{name}'s birthday is: {record.birthday.value}"

@input_error
def birthdays(book: AddressBook): # Показує всі дні народження, які відзначаються в найближчі 7 днів
    upcoming = book.get_upcoming_birthdays(days=7)
    if isinstance(upcoming, str):
        return upcoming 
    return "\n".join(f"{u['name']}: {u['birthday']}" for u in upcoming)