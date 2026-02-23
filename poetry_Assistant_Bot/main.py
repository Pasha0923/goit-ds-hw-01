from storage import load_data, save_data
from address_book import AddressBook
from handlers import parse_input
from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays , delete_phone
def main():
    book = load_data() # завантажуємо адресну книгу при старті
    # book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input: 
                continue 
        command, args = parse_input(user_input) 
        print(f"Command: {command} Arguments: {args}") 
        if command in ["close", "exit"]:
            save_data(book)  # зберігаємо книгу перед виходом команадами "close" або "exit"
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
           print(add_contact(args, book))  
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "delete_phone":
            print(delete_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))    
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()