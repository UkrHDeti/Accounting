import json

class Account:
    def __init__(self, code, name, balance=0):
        self.code = code
        self.name = name
        self.balance = balance

    def __repr__(self):
        return f"{self.code} {self.name}: {self.balance:.2f}"

    def to_dict(self):
        return {'code': self.code, 'name': self.name, 'balance': self.balance}

    @classmethod
    def from_dict(cls, d):
        return cls(d['code'], d['name'], d.get('balance', 0))

class Transaction:
    def __init__(self, debit_account, credit_account, amount, description):
        self.debit_account = debit_account
        self.credit_account = credit_account
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"{self.debit_account}->{self.credit_account}: {self.amount:.2f} ({self.description})"

    def to_dict(self):
        return {
            'debit_account': self.debit_account,
            'credit_account': self.credit_account,
            'amount': self.amount,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['debit_account'], d['credit_account'], d['amount'], d['description'])

class AccountingSystem:
    def __init__(self):
        self.accounts = {}
        self.journal = []

    def add_account(self, code, name):
        if code in self.accounts:
            print("Account already exists!")
            return
        self.accounts[code] = Account(code, name)

    def post_transaction(self, debit_code, credit_code, amount, description):
        if debit_code not in self.accounts or credit_code not in self.accounts:
            print("One of the accounts does not exist!")
            return
        self.accounts[debit_code].balance += amount
        self.accounts[credit_code].balance -= amount
        self.journal.append(Transaction(debit_code, credit_code, amount, description))

    def print_accounts(self):
        print("Chart of Accounts:")
        for acc in self.accounts.values():
            print(acc)

    def print_journal(self):
        print("Journal Entries:")
        for tx in self.journal:
            print(tx)

    def save_to_file(self, filename):
        data = {
            'accounts': [acc.to_dict() for acc in self.accounts.values()],
            'journal': [tx.to_dict() for tx in self.journal]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в файл {filename}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.accounts = {acc['code']: Account.from_dict(acc) for acc in data.get('accounts', [])}
            self.journal = [Transaction.from_dict(tx) for tx in data.get('journal', [])]
            print(f"Данные загружены из файла {filename}")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

def main():
    acc = AccountingSystem()
    FILENAME = "accounting_data.json"

    # Попробуем загрузить данные при запуске
    acc.load_from_file(FILENAME)

    while True:
        print("\n1. Показать план счетов\n2. Показать журнал проводок\n3. Добавить счет\n4. Провести операцию\n5. Сохранить данные\n6. Загрузить данные\n7. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            acc.print_accounts()
        elif choice == "2":
            acc.print_journal()
        elif choice == "3":
            code = input("Код счета: ")
            name = input("Название счета: ")
            acc.add_account(code, name)
        elif choice == "4":
            debit = input("Дебет (код счета): ")
            credit = input("Кредит (код счета): ")
            amount = float(input("Сумма: "))
            desc = input("Описание: ")
            acc.post_transaction(debit, credit, amount, desc)
        elif choice == "5":
            acc.save_to_file(FILENAME)
        elif choice == "6":
            acc.load_from_file(FILENAME)
        elif choice == "7":
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()