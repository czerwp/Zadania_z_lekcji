from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "projekt_magazyn_secret"


class Manager:
    def __init__(self, plik_danych):
        self.plik_danych = plik_danych
        self.saldo = 0.0
        self.magazyn = {}
        self.historia = []
        self.wczytaj_z_pliku()

    def wczytaj_z_pliku(self):
        if not os.path.exists(self.plik_danych):
            return
        with open(self.plik_danych, "r", encoding="utf-8") as f:
            for linia in f:
                dane = linia.strip().split("|")
                if not dane or not dane[0]: continue
                if dane[0] == "SALDO":
                    self.saldo = float(dane[1])
                elif dane[0] == "MAGAZYN":
                    self.magazyn[dane[1]] = {"cena": float(dane[2]), "ilosc": int(dane[3])}
                elif dane[0] == "HISTORIA":
                    self.historia.append("|".join(dane[1:]))

    def zapisz_do_pliku(self):
        with open(self.plik_danych, "w", encoding="utf-8") as f:
            f.write(f"SALDO|{self.saldo}\n")
            for nazwa, d in self.magazyn.items():
                f.write(f"MAGAZYN|{nazwa}|{d['cena']}|{d['ilosc']}\n")
            for wpis in self.historia:
                f.write(f"HISTORIA|{wpis}\n")

    def dodaj_do_historii(self, akcja):
        self.historia.append(akcja)
        self.zapisz_do_pliku()


manager = Manager("data.txt")


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
            manager.dodaj_do_historii(f"ZAKUP: {nazwa} | {ilosc} szt. | Cena: {cena}")
            flash(f"Zakupiono {nazwa} ({ilosc} szt.)", "success")
        else:
            flash("Błąd: Niewystarczające saldo!", "error")
    except ValueError:
        flash("Błąd: Nieprawidłowe dane zakupu.", "error")
    return redirect(url_for('index'))


@app.route('/sprzedaz', methods=['POST'])
def sprzedaz():
    try:
        nazwa = request.form.get('nazwa').strip().capitalize()
        ilosc = int(request.form.get('ilosc'))

        if nazwa in manager.magazyn and manager.magazyn[nazwa]['ilosc'] >= ilosc:
            cena = manager.magazyn[nazwa]['cena']
            manager.magazyn[nazwa]['ilosc'] -= ilosc
            manager.saldo += cena * ilosc
            manager.dodaj_do_historii(f"SPRZEDAŻ: {nazwa} | {ilosc} szt. | Cena: {cena}")
            flash(f"Sprzedano {nazwa} ({ilosc} szt.)", "success")
        else:
            flash("Błąd: Brak towaru w magazynie lub niewystarczająca ilość.", "error")
    except ValueError:
        flash("Błąd: Nieprawidłowe dane sprzedaży.", "error")
    return redirect(url_for('index'))


@app.route('/saldo', methods=['POST'])
def zmiana_saldo():
    try:
        wartosc = float(request.form.get('wartosc'))
        if manager.saldo + wartosc < 0:
            flash("Błąd: Saldo nie może być ujemne!", "error")
        else:
            manager.saldo += wartosc
            manager.dodaj_do_historii(f"SALDO: Zmiana o {wartosc} zł")
            flash("Zaktualizowano saldo.", "success")
    except ValueError:
        flash("Błąd: Nieprawidłowa wartość salda.", "error")
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