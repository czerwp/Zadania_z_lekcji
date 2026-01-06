import sys


class Manager:
    def __init__(self, plik_bazy):
        self.plik_bazy = plik_bazy
        self.actions = {}
        self.saldo = 0.0
        self.warehouse = {}
        self.history = []

        self.load_data()

    def assign(self, name):
        def decorator(func):
            self.actions[name] = func
            return func

        return decorator

    def execute(self, name):
        if name in self.actions:
            self.actions[name](self)
        else:
            print(f"Błąd: Nieznana komenda '{name}'.")

    def load_data(self):
        try:
            with open(self.plik_bazy, "r", encoding="utf-8") as f:
                for linia in f:
                    dane = linia.strip().split("|")
                    if not dane or dane[0] == "":
                        continue
                    if dane[0] == "SALDO":
                        self.saldo = float(dane[1])
                    elif dane[0] == "MAGAZYN":
                        nazwa, cena, ilosc = dane[1], float(dane[2]), int(dane[3])
                        self.warehouse[nazwa] = {"cena": cena, "ilość": ilosc}
                    elif dane[0] == "HISTORIA":
                        self.history.append(tuple(dane[1:]))
        except FileNotFoundError:
            print("Nie znaleziono pliku bazy. Rozpoczynanie z pustymi danymi.")

    def save_data(self):
        with open(self.plik_bazy, "w", encoding="utf-8") as f:
            f.write(f"SALDO|{self.saldo}\n")
            for nazwa, d in self.warehouse.items():
                f.write(f"MAGAZYN|{nazwa}|{d['cena']}|{d['ilość']}\n")
            for wpis in self.history:
                f.write(f"HISTORIA|{'|'.join(map(str, wpis))}\n")
        print("Dane zostały zapisane.")

manager = Manager("data.txt")

@manager.assign("saldo")
def handle_saldo(m):
    try:
        amount = float(input("Podaj kwotę do dodania lub odjęcia: "))
        if m.saldo + amount < 0:
            print("Błąd: Saldo nie może być ujemne.")
        else:
            m.saldo += amount
            m.history.append(("saldo", amount))
            print(f"Aktualne saldo: {m.saldo} zł")
    except ValueError:
        print("Błąd: Niepoprawna kwota.")


@manager.assign("sprzedaż")
def handle_sale(m):
    product_name = input("Podaj nazwę produktu: ")
    if product_name not in m.warehouse or m.warehouse[product_name]['ilość'] <= 0:
        print("Błąd: Brak produktu w bazie.")
        return
    try:
        price = float(input("Podaj cenę: "))
        pieces = int(input("Podaj ilość: "))
        if pieces <= 0 or price <= 0:
            print("Błąd: Wartości muszą być dodatnie.")
        elif m.warehouse[product_name]['ilość'] < pieces:
            print("Błąd: Niewystarczająca ilość towaru.")
        else:
            m.warehouse[product_name]['ilość'] -= pieces
            m.saldo += price * pieces
            m.history.append(("sprzedaż", product_name, price, pieces))
            print("Sprzedano produkt.")
    except ValueError:
        print("Błąd: Nieprawidłowe dane.")


@manager.assign("zakup")
def handle_purchase(m):
    product_name = input("Podaj nazwę produktu: ")
    try:
        price = float(input("Podaj cenę zakupu: "))
        pieces = int(input("Podaj ilość sztuk: "))
        cost = price * pieces
        if cost > m.saldo:
            print("Błąd: Niewystarczające środki na koncie.")
        else:
            m.saldo -= cost
            if product_name in m.warehouse:
                m.warehouse[product_name]['ilość'] += pieces
                m.warehouse[product_name]['cena'] = price
            else:
                m.warehouse[product_name] = {"cena": price, "ilość": pieces}
            m.history.append(("zakup", product_name, price, pieces))
            print("Dokonano zakupu.")
    except ValueError:
        print("Błąd: Nieprawidłowe dane.")


@manager.assign("konto")
def handle_account(m):
    print(f"Aktualne saldo: {m.saldo} zł")


@manager.assign("lista")
def handle_list(m):
    if not m.warehouse:
        print("Magazyn jest pusty.")
    else:
        print("Stan magazynu:")
        for nazwa, dane in m.warehouse.items():
            print(f"- {nazwa}: {dane['ilość']} szt., cena: {dane['cena']} zł")


@manager.assign("magazyn")
def handle_warehouse(m):
    product_name = input("Podaj nazwę produktu: ")
    if product_name in m.warehouse:
        d = m.warehouse[product_name]
        print(f"{product_name}: {d['ilość']} szt., cena: {d['cena']} zł")
    else:
        print("Brak produktu w magazynie.")


@manager.assign("przegląd")
def handle_review(m):
    try:
        start_inp = input("Podaj początek zakresu: ")
        stop_inp = input("Podaj koniec zakresu: ")
        start = int(start_inp) if start_inp else 0
        stop = int(stop_inp) if stop_inp else len(m.history)

        if start < 0 or stop > len(m.history):
            print(f"Błąd: Zakres poza historią (0-{len(m.history)}).")
        else:
            for i in range(start, stop):
                print(f"{i}: {m.history[i]}")
    except ValueError:
        print("Błąd: Podaj poprawne liczby.")


while True:
    print("\n--- Menu Zarządzania Firmą ---")
    opt = input("Wybierz opcję (saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec): ").strip().lower()

    if opt == "koniec":
        manager.save_data()
        print("Aplikacja zakończyła działanie.")
        break

    manager.execute(opt)