
saldo = 0.0
warehouse={}
history=[]
while True:
    options=input('Wybierz jedną z następujących opcji: \n * saldo \n * sprzedaż \n * zakup \n * konto \n * lista \n * magazyn \n * przegląd \n * koniec \n').strip().lower()

    if options == 'saldo':
        amount=float(input("Podaj kwotę do dodania lub odjęcia (wpisz ze znakiem minus)z konta: "))
        if type(amount)==float or type(amount)==int:
            saldo += amount
            history.append(amount)
            print(f'Aklualne saldo: {saldo} zł')
            continue
        elif saldo + amount < 0:
            print("Nieprawidłowa wartość salda")
            continue
        else:
            print("Niepoprawna kwota")
            continue
    if options == 'sprzedaż':
        product_name=input("Podaj nazwę produktu? ")
        price=float(input("Podaj cene produktu? "))
        pieces=int(input("Podaj ilość sztuk "))
        if product_name not in warehouse or warehouse[product_name]['ilość'] <= 0:
            print('Brak produktu w bazie')
            continue
        if price<=0 or pieces <=0:
            print('Nieprawidłowe wartości, cena i ilość nie mogą być dodatnie')
            continue
        if warehouse[product_name]['ilość']<pieces:
            print('Podana ilość jest niedostępna')
            continue
        if warehouse[product_name]['ilość']<pieces:
            print("Brak wystarczającej ilości towaru na stanie")
            continue
        warehouse[product_name]['ilość'] -= pieces
        saldo += price * pieces
        history.append(("sprzedaż", product_name, price, pieces))
        print(f'Sprzedano produkt {product_name} w ilości {pieces} szt. w cenie {price} zł/szt')
        continue
    elif options == 'zakup':
        product_name = input("Podaj nazwę produktu? ")
        price= float(input("Podaj cene produktu? "))
        pieces = int(input("Podaj ilość sztuk "))
        if not isinstance(price, (float, int)):
            print('Nieprawidłowe wartości')
            continue
        if not isinstance(pieces,  int):
                print('Nieprawidłowe wartości')
                continue
        if price <= 0 or pieces <=0:
            print("Popraw wpisane wartości, powinny być dodatnie")
            continue
        cost = price * pieces
        if saldo - cost <0:
            print("Zakup niemożliwy, niewystarczająca ilość środków")
            continue
        saldo -= cost
        if product_name in warehouse:
            warehouse[product_name]['ilość'] +=pieces
            warehouse[product_name]['cena']=price
        else:
            warehouse[product_name] = {"cena": price, "ilość": pieces}
        history.append(("zakup", product_name, price, pieces))
        print(f'Zakupiono produkt {product_name} w ilości {pieces} szt. w cenie {price} zł/szt')
        continue
    if options == 'konto':
        print(f' Aktualne saldo: {saldo} zł')
        continue
    elif options == 'lista':
        if not warehouse:
            print("Magazyn jest pusty")
            continue
        else:
            print("Stan magazynu")
            for product_name, values in warehouse.items():
                print(f' {product_name}: {values['ilość']} szt., cena: {values['cena']} zł/')
            continue
    if options == 'magazyn':
        product_name = input("Podaj nazwę produktu? ")
        if product_name in warehouse:
            print(f'{product_name}: {warehouse[product_name]['ilość']} szt., cena: {warehouse[product_name]['cena']:} zł')
            continue
        else:
            print('Nie ma takiego produktu w magazynie')
            continue
    elif options == 'przegląd':
        start=int(input('Podaj początkowy numer operacji '))
        stop = int(input('Podaj końcowy numer operacji '))
        startt=start if start else 0
        end=stop if stop else len(history)
        if startt< 0 or end > len(history):
            print(f"Zakres nie istnieje. Dostępny zakres: {len(history)}")
            continue
        print('Przegląd operacji od {startt} do {end-1}:')
        for x in range(start, end):
            print(x, history[x])
            continue
    elif options == 'koniec':
        print("Aplikacja zakończyła działanie")
        break
    else:
      print("Nie znana komenda, zobacz czy jest wpisana małą literą i nie zawiera literówki. Spróbuj ponownie")

