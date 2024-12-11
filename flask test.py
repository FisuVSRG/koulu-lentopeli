from flask import Flask, render_template, request, jsonify
from mysql.connector import Error
import mysql.connector
from flask_cors import CORS
from kayttaja import Kayttaja
from peli import Peli
from vertaa import vastaus
from tulostaulukko import tulostaulukko
from yhteys import connect_to_db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080"]}}, supports_credentials=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/another-page')
def another_page():
    return render_template('another_page.html')


@app.route('/leaderboards')
def top_scores():
    scores = tulostaulukko(10)
    return render_template('leaderboards.html', scores=scores)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
