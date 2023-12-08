from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) or "Undefined"

class Name(Field):
    def __init__(self,value):
        self.value = str(value)

class PhoneCheck:
    def p_check(self,phone:str):
        from re import search
        map = {' ':''}
        phone.translate(map)
        if len(phone) == 10 and search(r'\d{10}', phone) != None:
            return phone
        else:
            print("Incorrect phone number. Must be exactly 10 characters, digits only.")
            raise ValueError

class Phone(Field, PhoneCheck):
    def __init__(self,phone:str):
        if type(self.p_check(phone)) == str:
            self.value = self.p_check(phone)

class Record(PhoneCheck):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self,phone):
        if type(self.p_check(phone)) == str:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
            print(f"Added number {phone_obj.value} to the record (named '{self.name.value}')!")
    
    def p_find(self,phone:str):
        for i in self.phones:
            if i.value == phone:
                return i
            
        print(f"No number {phone} in {self.name.value} record!")
        return False

    def edit_phone(self,phone:str,new_phone:str):
        if self.p_find(phone):
            if type(self.p_check(new_phone)) == str:
                self.phones.remove(self.p_find(phone))
                phone_obj = Phone(new_phone)
                self.phones.append(phone_obj)
                return
        
        raise ValueError
    def find_phone(self,phone):
        if self.p_find(phone):
            return self.p_find(phone)

    def remove_phone(self,phone):
        if self.p_find(phone):
            self.phones.remove(self.p_find(phone))
        else:
            print(f"No number {phone} in {self.name.value} record!")


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self,record:Record):
        if not record.name.value in self.data.keys():
            self.data[record.name.value] = record
            print(f"Record {record.name.value} with phone numbers {'; '.join(p.value for p in record.phones)} added!")
        else:
            print(f"This record already exists! Delete it first, then re-add.")

    
    def find(self,name:str):
        if name in self.data.keys():
            return self.data[name]
        else:
            print(f"Record {name} not found!")
            return None
    
    def delete(self,name:str):
        if name in self.data.keys():
            del self.data[name]
            print(f"Record {name} deleted!")
        else:
            print(f"Record {name} not found!")
            return None

    # Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")