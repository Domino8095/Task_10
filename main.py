from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Телефон повинен містити лише 10 цифр')
    
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    def __set__(self, instance, value):
        self.validate(value)
        super().__set__(instance, value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Имя контакта: {self.name.value}, телефоны: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def remove_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
    
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone = self.find_phone(old_phone_number)
        if phone:
            phone.value = new_phone_number
        else:
            raise ValueError("Телефон не найден")
        

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def find(self, name: str):
        if name in self.data:
            return self.data[name]

    def display_all_records(self):
        for record in self.data.values():
            print(record)

# Тестируем код
book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Выводим все записи в адресной книге
book.display_all_records()

# Находим запись по имени и редактируем номер телефона
john = book.find("John")
if john:
    john.remove_phone("1234567890")
    john.add_phone("1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    if found_phone:
        print(f"{john.name}: {found_phone}")

# Удаляем запись
book.delete("Jane")
book.display_all_records()
