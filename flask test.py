from flask import Flask, render_template, request, jsonify, url_for, session
from mysql.connector import Error
import mysql.connector
from flask_cors import CORS
from kayttaja import Kayttaja
from peli import Peli
from vertaa import vastaus
from tulostaulukko import tulostaulukko
from yhteys import connect_to_db

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}}, supports_credentials=True)
app.secret_key = 'supersecretkey'  # Required for flash messages


def get_db_connection():
    conn = connect_to_db()
    if not conn:
        raise ConnectionError("Failed to connect to the database.")
    return conn

# Route to serve main page
@app.route('/')
def index():
    leaderboard_url = url_for('leaderboards')
    print(f"Leaderboard URL: {leaderboard_url}")
    play_url = url_for('play')
    print(f"Play URL: {play_url}")
    play_url = url_for('play')
    print(f"Play URL: {play_url}")
    return render_template('index.html')

@app.route('/leaderboards')
def leaderboards():
    index_url = url_for('index')
    print(f"Index URL: {index_url}")
    return render_template('leaderboards.html')

@app.route('/help')
def help():
    index_url = url_for('index')
    print(f"Index URL: {index_url}")
    return render_template('help.html')

@app.route('/play')
def play():
    index_url = url_for('index')
    print(f"Index URL: {index_url}")
    return render_template('play.html')

@app.route('/api/leaderboards')
def api_top_scores():
    scores = tulostaulukko(10)
    return jsonify(scores)

@app.route('/handle_form_ajax', methods=['POST'])
def handle_form_ajax():
    username = request.form['username']
    try:
        kayttaja = Kayttaja()
        kayttaja.tallenna_kayttajatunnus(username)
        session['username'] = kayttaja.username
        return jsonify(username=kayttaja.username)
    except Exception as e:
        return jsonify(message=str(e)), 400

if __name__ == "__main__":
    app.run(debug=True)
