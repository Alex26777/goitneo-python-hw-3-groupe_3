from datetime import datetime, timedelta
from collections import UserDict

class Field:
    # Базовий клас для всіх полів
    def __init__(self, value):
        self.value = value

class Name(Field):
    # Клас для зберігання імені контакту
    pass

class Phone(Field):
    # Клас для зберігання телефонного номеру
    def __init__(self, value):
        # Перевірка на валідність телефонного номеру
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися з 10 цифр")
        super().__init__(value)

class Birthday(Field):
    # Клас для зберігання дня народження
    def __init__(self, value):
        # Перевірка на валідність формату дати
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Дата народження має бути у форматі DD.MM.YYYY")
        super().__init__(value)

class Record:
    # Клас для зберігання інформації про контакт
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
    # Клас для зберігання та управління контактами
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

# Тут повинні бути функції обробники для взаємодії з класами вище
# Наприклад, обробка команд 'add', 'change', 'phone', 'all', 'add-birthday', 'show-birthday', 'birthdays' тощо
