import pickle
from address_book import AddressBook

def save_data(book: AddressBook, filename="addressbook.pkl"): # серіалізує та зберігає об'єкт AddressBook у файл
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl") -> AddressBook: # завантажує адресну книгу з файлу або створює нову, якщо файл не знайдено
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()