from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "tajny_klucz_do_wiadomosci_flash"


class Manager:
    def __init__(self):
        self.saldo = 10000.0
        self.magazyn = {"Masło": {"cena": 2.5, "ilosc": 10}}
        self.historia = []

    def dodaj_do_historii(self, wpis):
        self.historia.append(wpis)
        print(f"Dodano do historii: {wpis}")


manager = Manager()


@app.route('/')
def index():
    return render_template('index.html', saldo=manager.saldo, magazyn=manager.magazyn)


@app.route('/zakup', methods=['POST'])
def zakup():
    try:
        nazwa = request.form.get('nazwa').strip().capitalize()
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))
        koszt = cena * ilosc

        if manager.saldo >= koszt:
            manager.saldo -= koszt
            if nazwa in manager.magazyn:
                manager.magazyn[nazwa]['ilosc'] += ilosc
                manager.magazyn[nazwa]['cena'] = cena
            else:
                manager.magazyn[nazwa] = {"cena": cena, "ilosc": ilosc}

            manager.dodaj_do_historii(f"ZAKUP: {nazwa}, {ilosc} szt., cena: {cena} zł/szt")
            flash(f"Zakupiono {nazwa}", "success")
        else:
            flash("Niewystarczające saldo!", "error")

    except (ValueError, TypeError):
        flash("Nieprawidłowe dane w formularzu zakupu.", "error")

    return redirect(url_for('index'))


@app.route('/sprzedaz', methods=['POST'])
def sprzedaz():
    try:
        nazwa = request.form.get('nazwa').strip().capitalize()
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))

        if nazwa not in manager.magazyn:
            flash(f"BŁĄD: Towaru '{nazwa}' nie ma w naszej bazie danych!", "error")

        elif manager.magazyn[nazwa]['ilosc'] <= 0:
            flash(f"BŁĄD: Towar '{nazwa}' jest w bazie, ale aktualnie nie ma go na stanie (0 szt.)!", "error")

        elif manager.magazyn[nazwa]['ilosc'] < ilosc:
            dostepne = manager.magazyn[nazwa]['ilosc']
            flash(f"BŁĄD: Za mała ilość! Chcesz kupić {ilosc}, a na stanie mamy tylko {dostepne} szt.", "error")

        else:
            manager.magazyn[nazwa]['ilosc'] -= ilosc
            manager.saldo += cena * ilosc
            manager.dodaj_do_historii(f"SPRZEDAŻ: {nazwa}, {ilosc} szt., cena: {cena} zł/szt")
            flash(f"Sprzedano pomyślnie: {nazwa} ({ilosc} szt.)", "success")

    except (ValueError, TypeError):
        flash("BŁĄD: Wprowadzono nieprawidłowe dane liczbowe.", "error")

    return redirect(url_for('index'))


@app.route('/saldo', methods=['POST'])
def zmiana_saldo():
    try:
        komentarz = request.form.get('komentarz')
        wartosc = float(request.form.get('wartosc'))

        if manager.saldo + wartosc < 0:
            flash("Saldo nie może być ujemne!", "error")
        else:
            manager.saldo += wartosc
            manager.dodaj_do_historii(f"SALDO: {wartosc} zł ({komentarz})")
            flash("Zaktualizowano saldo.", "success")
    except ValueError:
        flash("Nieprawidłowa wartość salda.", "error")

    return redirect(url_for('index'))


@app.route('/historia/')
@app.route('/historia/<int:line_from>/<int:line_to>/')
def historia(line_from=None, line_to=None):
    arg_from = request.args.get('line_from')
    arg_to = request.args.get('line_to')

    if arg_from is not None and arg_to is not None:
        if arg_from != '' and arg_to != '':
            return redirect(url_for('historia', line_from=arg_from, line_to=arg_to))
        else:
            return redirect(url_for('historia'))

    logi = manager.historia
    max_len = len(logi)

    start = int(line_from) if line_from is not None else 0
    stop = int(line_to) if line_to is not None else max_len

    start = max(0, min(start, max_len))
    stop = max(0, min(stop, max_len))

    if start > stop:
        start, stop = stop, start

    wyswietlana_historia = logi[start:stop]
    info_tekst = f"Zakres: od {start} do {stop} (łącznie wpisów: {max_len})"

    return render_template('historia.html',
                           historia=wyswietlana_historia,
                           info=info_tekst,
                           line_from=start,
                           max_len=max_len)


if __name__ == '__main__':
    app.run(debug=True)