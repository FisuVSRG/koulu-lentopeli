from flask import Flask, render_template
from mysql.connector import Error
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def connect_to_db():
    try:
        # Yhdistä MariaDB-tietokantaan
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='root',
            password='kuha',
            autocommit=True
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Virhe yhteydessä MySQL:hen: {e}")
        return None

def tulostaulukko():
    connection = connect_to_db()

    if connection.is_connected():
        cursor = connection.cursor()

        # Haetaan peleistä ne 10, joissa on korkein tulos, ja tulostetaan niiden käyttäjänimi ja tulos.
        tulokset = """SELECT username, score
                      FROM user
                      INNER JOIN game ON game.user_id = user.id
                      ORDER BY score DESC
                      LIMIT 10
                      """
        cursor.execute(tulokset)
        parhaat = cursor.fetchall()

        # Return the results as a list of dictionaries
        results = []
        for i in parhaat:
            nimi, score = i
            score_str = str(score)

            if "None" not in score_str:
                results.append({"username": nimi, "score": score})

        return results

@app.route('/top-scores')
def top_scores():
    scores = tulostaulukko()
    return render_template('top_scores.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
