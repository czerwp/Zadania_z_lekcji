
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "super_tajny_klucz_firmy"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'firma.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wartosc = db.Column(db.Float, nullable=False, default=0.0)


class Magazyn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), unique=True, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)


class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wpis = db.Column(db.String(500), nullable=False)
    kwota_zmiany = db.Column(db.Float, default=0.0)  # Pomocne do skryptu sprawdzającego



def pobierz_lub_stworz_saldo():
    s = Saldo.query.first()
    if not s:
        s = Saldo(wartosc=0.0)
        db.session.add(s)
        db.session.commit()
    return s


def sprawdz_spojnosc_danych():
    wszystkie_wpisy = Historia.query.all()
    suma_historii = sum(h.kwota_zmiany for h in wszystkie_wpisy)
    aktualne_saldo = pobierz_lub_stworz_saldo().wartosc
    return round(suma_historii, 2) == round(aktualne_saldo, 2)


@app.route('/')
def index():
    saldo_obj = pobierz_lub_stworz_saldo()
    produkty = Magazyn.query.all()
    spojne = sprawdz_spojnosc_danych()
    return render_template('index.html',
                           saldo=saldo_obj.wartosc,
                           magazyn=produkty,
                           db_status=spojne)


@app.route('/zakup', methods=['POST'])
def zakup():
    try:
        nazwa = request.form.get('nazwa').strip().capitalize()
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))
        koszt = cena * ilosc

        saldo_obj = pobierz_lub_stworz_saldo()

        if saldo_obj.wartosc >= koszt:
            produkt = Magazyn.query.filter_by(nazwa=nazwa).first()

            # TRANSAKCJA START
            saldo_obj.wartosc -= koszt
            if produkt:
                produkt.ilosc += ilosc
                produkt.cena = cena  # Aktualizacja do najnowszej ceny
            else:
                db.session.add(Magazyn(nazwa=nazwa, cena=cena, ilosc=ilosc))

            db.session.add(Historia(wpis=f"ZAKUP: {nazwa}, {ilosc} szt. za {koszt} zł", kwota_zmiany=-koszt))

            db.session.commit()
            flash(f"Pomyślnie zakupiono {ilosc}x {nazwa}", "success")
        else:
            flash("Błąd: Niewystarczające środki na koncie!", "error")

    except Exception as e:
        db.session.rollback()
        flash(f"Wystąpił błąd podczas zakupu: {str(e)}", "error")

    return redirect(url_for('index'))


@app.route('/sprzedaz', methods=['POST'])
def sprzedaz():
    try:
        nazwa = request.form.get('nazwa').strip().capitalize()
        ilosc = int(request.form.get('ilosc'))

        produkt = Magazyn.query.filter_by(nazwa=nazwa).first()
        saldo_obj = pobierz_lub_stworz_saldo()

        if produkt and produkt.ilosc >= ilosc:
            zysk = produkt.cena * ilosc

            produkt.ilosc -= ilosc
            saldo_obj.wartosc += zysk

            db.session.add(Historia(wpis=f"SPRZEDAŻ: {nazwa}, {ilosc} szt. za {zysk} zł", kwota_zmiany=zysk))

            db.session.commit()
            flash(f"Pomyślnie sprzedano {ilosc}x {nazwa}", "success")
        else:
            flash("Błąd: Brak towaru w magazynie lub niewystarczająca ilość!", "error")

    except Exception as e:
        db.session.rollback()
        flash(f"Wystąpił błąd podczas sprzedaży: {str(e)}", "error")

    return redirect(url_for('index'))


@app.route('/historia/')
@app.route('/historia/<int:start>/<int:koniec>/')
def historia(start=None, koniec=None):
    f_start = request.args.get('f_start')
    f_koniec = request.args.get('f_koniec')

    if f_start is not None and f_koniec is not None:
        return redirect(url_for('historia', start=f_start, koniec=f_koniec))

    wszystkie_wpisy = Historia.query.all()
    max_len = len(wszystkie_wpisy)

    if start is not None and koniec is not None:
        idx_start = max(0, start - 1)
        idx_koniec = min(max_len, koniec)
        wybrane_wpisy = wszystkie_wpisy[idx_start:idx_koniec]
        display_start = start
    else:
        wybrane_wpisy = wszystkie_wpisy
        display_start = 1

    return render_template('historia.html',
                           historia=wybrane_wpisy,
                           start=display_start,
                           max_len=max_len)

@app.route('/saldo', methods=['POST'])
def saldo():
    try:
        kwota = float(request.form.get('kwota'))
        saldo_obj = pobierz_lub_stworz_saldo()

        if saldo_obj.wartosc + kwota < 0:
            flash("Błąd: Nie można wypłacić kwoty większej niż stan konta!", "error")
        else:
            saldo_obj.wartosc += kwota
            typ = "WPŁATA" if kwota > 0 else "WYPŁATA"
            db.session.add(Historia(wpis=f"{typ}: Zmiana salda o {kwota} zł", kwota_zmiany=kwota))
            db.session.commit()
            flash(f"Pomyślnie wykonano operację: {typ}", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Błąd zmiany salda: {str(e)}", "error")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)