class Uczen:
    def __init__(self, imie_nazwisko, klasa):
        self.imie_nazwisko = imie_nazwisko
        self.klasa = klasa


class Nauczyciel:
    def __init__(self, imie_nazwisko, przedmiot, klasy):
        self.imie_nazwisko = imie_nazwisko
        self.przedmiot = przedmiot
        self.klasy = klasy


class Wychowawca:
    def __init__(self, imie_nazwisko, klasa):
        self.imie_nazwisko = imie_nazwisko
        self.klasa = klasa


def main():
    uczniowie = []
    nauczyciele = []
    wychowawcy = []

    while True:
        komenda = input("\nGłówne menu (utworz, zarzadzaj, koniec): ").strip().lower()

        if komenda == "utworz":
            while True:
                opcja = input("Utwórz (uczen, nauczyciel, wychowawca, koniec): ").strip().lower()
                if opcja == "uczen":
                    imie = input("Imię i nazwisko ucznia: ")
                    klasa = input("Klasa: ")
                    uczniowie.append(Uczen(imie, klasa))
                elif opcja == "nauczyciel":
                    imie = input("Imię i nazwisko nauczyciela: ")
                    przedmiot = input("Nazwa przedmiotu: ")
                    klasy_nauczyciela = []
                    print("Wypisz klasy, które prowadzi nauczyciel (pusta linia zamyka listę):")
                    while True:
                        k = input("> ")
                        if not k:
                            break
                        klasy_nauczyciela.append(k)
                    nauczyciele.append(Nauczyciel(imie, przedmiot, klasy_nauczyciela))
                elif opcja == "wychowawca":
                    imie = input("Imię i nazwisko wychowawcy: ")
                    klasa = input("Prowadzona klasa: ")
                    wychowawcy.append(Wychowawca(imie, klasa))
                elif opcja == "koniec":
                    break

        elif komenda == "zarzadzaj":
            while True:
                opcja = input("Zarządzaj (klasa, uczen, nauczyciel, wychowawca, koniec): ").strip().lower()
                if opcja == "klasa":
                    szukana_klasa = input("Podaj nazwę klasy: ")
                    print(f"\nKlasa {szukana_klasa}:")
                    # Wypisz uczniów
                    for u in uczniowie:
                        if u.klasa == szukana_klasa:
                            print(f"- Uczeń: {u.imie_nazwisko}")
                    # Wypisz wychowawcę
                    for w in wychowawcy:
                        if w.klasa == szukana_klasa:
                            print(f"- Wychowawca: {w.imie_nazwisko}")

                elif opcja == "uczen":
                    szukany_uczen = input("Podaj imię i nazwisko ucznia: ")
                    znaleziony_u = next((u for u in uczniowie if u.imie_nazwisko == szukany_uczen), None)
                    if znaleziony_u:
                        print(f"Przedmioty ucznia {szukany_uczen}:")
                        for n in nauczyciele:
                            if znaleziony_u.klasa in n.klasy:
                                print(f"- Przedmiot: {n.przedmiot}, Nauczyciel: {n.imie_nazwisko}")
                    else:
                        print("Nie znaleziono takiego ucznia.")

                elif opcja == "nauczyciel":
                    szukany_n = input("Podaj imię i nazwisko nauczyciela: ")
                    znaleziony_n = next((n for n in nauczyciele if n.imie_nazwisko == szukany_n), None)
                    if znaleziony_n:
                        print(f"Nauczyciel {szukany_n} prowadzi klasy: {', '.join(znaleziony_n.klasy)}")
                    else:
                        print("Nie znaleziono nauczyciela.")

                elif opcja == "wychowawca":
                    szukany_w = input("Podaj imię i nazwisko wychowawcy: ")
                    wych = next((w for w in wychowawcy if w.imie_nazwisko == szukany_w), None)
                    if wych:
                        print(f"Uczniowie prowadzeni przez {szukany_w}:")
                        for u in uczniowie:
                            if u.klasa == wych.klasa:
                                print(f"- {u.imie_nazwisko}")
                    else:
                        print("Nie znaleziono wychowawcy.")

                elif opcja == "koniec":
                    break

        elif komenda == "koniec":
            print("Zamykanie programu...")
            break
        else:
            print("Niepoprawna komenda.")


if __name__ == "__main__":
    main()