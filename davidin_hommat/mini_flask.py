from flask import Flask, render_template
from kentta import Lentokentta

app = Flask(__name__)

@app.route('/')
def peli():
    kentta1 = Lentokentta('EFHK')  # Example ICAO code for Helsinki
    kentta2 = Lentokentta('ESSA')  # Example ICAO code for Stockholm

    coordinates1 = kentta1.hae_koordinaatit() or [0, 0]
    coordinates2 = kentta2.hae_koordinaatit() or [0, 0]
    country1 = kentta1.hae_maa() or "Unknown Country"
    country2 = kentta2.hae_maa() or "Unknown Country"

    kentta1.close_connection()
    kentta2.close_connection()

    return render_template('peli.html',
                           coordinates1=coordinates1,
                           coordinates2=coordinates2,
                           country1=country1,
                           country2=country2)

if __name__ == '__main__':
    app.run(debug=True)