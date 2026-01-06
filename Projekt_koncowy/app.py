from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///szkola_2026.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class DaneSzkolne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uczen = db.Column(db.String(100))
    klasa = db.Column(db.String(20))
    przedmioty = db.Column(db.Text)
    oceny = db.Column(db.String(100))
    wychowawca = db.Column(db.String(100))


def pobierz_pogode():
    import requests
    from datetime import date
    today = date.today().isoformat()

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude=52.41&longitude=16.92"
        f"&current=temperature_2m"
        f"&daily=rain_sum&timezone=Europe/Berlin"
        f"&start_date={today}&end_date={today}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        temp_val = None
        if 'current' in data:
            temp_val = data['current'].get('temperature_2m')
        elif 'current_weather' in data:
            temp_val = data['current_weather'].get('temperature')

        opady = data.get('daily', {}).get('rain_sum', [0])[0]

        return {
            "temp": f"{temp_val}°C" if temp_val is not None else "--°C",
            "opady": f"{opady} mm",
            "data": today
        }
    except Exception as e:
        print(f"BŁĄD POGODY: {e}")
        return {"temp": "Błąd", "opady": "0 mm", "data": today}


@app.route('/')
def index():
    pogoda_dane = pobierz_pogode()
    return render_template('index.html', pogoda=pogoda_dane)

@app.route('/szukaj', methods=['POST'])
def szukaj():
    typ = request.form.get('typ')
    fraza = request.form.get('fraza')
    wyniki = []

    if typ == 'uczen':
        wyniki = DaneSzkolne.query.filter_by(uczen=fraza).all()
    elif typ == 'nauczyciel':
        wyniki = DaneSzkolne.query.filter((DaneSzkolne.wychowawca == fraza) | (DaneSzkolne.przedmioty.contains(fraza))).all()
    elif typ == 'klasa':
        wyniki = DaneSzkolne.query.filter_by(klasa=fraza).all()

    return render_template('wynik.html', wyniki=wyniki, typ=typ, fraza=fraza)


@app.route('/dodaj_formularz', methods=['GET', 'POST'])
def dodaj_formularz():
    if request.method == 'POST':
        nazwy_przedmiotow = request.form.getlist('nazwa_przedmiotu[]')
        nauczyciele = request.form.getlist('nauczyciel_przedmiotu[]')
        oceny = request.form.getlist('ocena[]')


        lista_przedmiotow_info = []
        for p, n, o in zip(nazwy_przedmiotow, nauczyciele, oceny):
            lista_przedmiotow_info.append(f"{p} ({n}) - Ocena: {o}")

        pelny_opis_przedmiotow = "; ".join(lista_przedmiotow_info)

        nowy = DaneSzkolne(
            uczen=request.form['uczen'],
            klasa=request.form['klasa'],
            wychowawca=request.form['wychowawca'],
            przedmioty=pelny_opis_przedmiotow,
            oceny="Zapisano w polu przedmioty"
        )

        db.session.add(nowy)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('dodaj.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)