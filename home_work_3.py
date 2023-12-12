from datetime import datetime, timedelta
from collections import UserDict
import pickle

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        # Перевірка на валідність телефонного номеру
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися з 10 цифр")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        # Перевірка на валідність формату дати
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Дата народження має бути у форматі DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []  # Список телефонних номерів
        self.birthday = None  # День народження (необов'язковий)

    def add_phone(self, phone):
        # Метод для додавання номеру телефону
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        # Метод для додавання дня народження
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        # Повертає кількість днів до дня народження
        if not self.birthday:
            return None
        bday = datetime.strptime(self.birthday.value, '%d.%m.%Y')
        now = datetime.now()
        next_bday = bday.replace(year=now.year)
        if next_bday < now:
            next_bday = next_bday.replace(year=now.year + 1)
        return (next_bday - now).days

class AddressBook(UserDict):
    def get_birthdays_per_week(self):
        # Повертає імена контактів, у яких день народження наступного тижня
        today = datetime.now()
        result = {}
        for name, record in self.data.items():
            days = record.days_to_birthday()
            if days is not None and 0 <= days <= 7:
                weekday = (today + timedelta(days=days)).strftime('%A')
                result.setdefault(weekday, []).append(name)
        return result

    def save_to_disk(self, filename='address_book.pkl'):
        # Збереження адресної книги на диск у форматі pickle
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_disk(self, filename='address_book.pkl'):
        try:
            # Завантаження адресної книги з диска у форматі pickle
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            # Якщо файл не знайдено, створити нову адресну книгу
            print("Файл не знайдено. Створено нову адресну книгу.")

class MyBot:
    def __init__(self):
        # Ініціалізація бота та завантаження адресної книги з диска
        self.book = AddressBook()
        self.book.load_from_disk()

    def parse_input(self, user_input):
        # Розбір введеної команди та аргументів
        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]
        return command, args

    def add_contact(self, args):
        try:
            # Додавання нового контакту
            name, phone = args
            contact = Record(name)
            contact.add_phone(phone)
            self.book[name] = contact
            return f"Контакт {name} додано."
        except ValueError as e:
            return str(e)

    def show_all(self):
        # Виведення всіх контактів
        return '\n'.join(f'{name}: {record.phones[0].value}' for name, record in self.book.items()) if self.book else "Контактів не знайдено."

    def add_birthday(self, args):
        try:
            # Додавання дня народження до контакту
            name, birthday = args
            contact = self.book.get(name)
            if contact:
                contact.add_birthday(birthday)
                return f"День народження для {name} додано."
            else:
                return f"Контакт {name} не знайдено."
        except ValueError as e:
            return str(e)

    def show_birthday(self, args):
        # Показ дня народження для вказаного контакту
        name = args[0]
        contact = self.book.get(name)
        if contact and contact.birthday:
            return f"{name}: {contact.birthday.value}"
        elif contact:
            return f"Для {name} не вказано день народження."
        else:
            return f"Контакт {name} не знайдено."

    def birthdays(self):
        # Виведення днів народження на наступний тиждень
        upcoming_birthdays = self.book.get_birthdays_per_week()
        if upcoming_birthdays:
            return "\n".join(f"{day}: {', '.join(names)}" for day, names in upcoming_birthdays.items())
        else:
            return "В наступному тижні дні народження відсутні."

    def close(self):
        # Завершення роботи програми та збереження адресної книги на диск
        print("До побачення!")
        self.book.save_to_disk()
        exit()

    def process_command(self, command, args):
        # Обробка введених команд
        if command == "add":
            return self.add_contact(args)
        elif command == "all":
            return self.show_all()
        elif command in ["close", "exit"]:
            self.close()
        elif command == "add-birthday":
            return self.add_birthday(args)
        elif command == "show-birthday":
            return self.show_birthday(args)
        elif command == "birthdays":
            return self.birthdays()
        else:
            return "Невірна команда."

    def main(self):
        # Основний цикл взаємодії з користувачем
        print("Ласкаво просимо до бота-помічника!")

        while True:
            user_input = input("Введіть команду: ")
            command, args = self.parse_input(user_input)
            result = self.process_command(command, args)
            print(result)

if __name__ == "__main__":
    # Запуск бота при виклику скрипта
    bot = MyBot()
    bot.main()
