from flask import Flask, render_template, request, jsonify, url_for, session
from mysql.connector import Error
import mysql.connector
from flask_cors import CORS
from kayttaja import Kayttaja
from peli import Peli
from vertaa import vertaa_lentokenttien_korkeudet, vastaus
from tulostaulukko import tulostaulukko
from yhteys import connect_to_db
from kentta import Lentokentta

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
    help_url = url_for('help')
    print(f"Help URL: {help_url}")
    username_url = url_for('username')
    print(f"Username URL: {username_url}")
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

@app.route('/play', methods=['GET'])
def play():
    username = request.args.get('username')  # Get the username from the form
    if username:
        # Pass the username to the play.html template
        return render_template('play.html', username=username)
    else:
        return "Username is required", 400

@app.route('/username')
def username():
    index_url = url_for('index')
    print(f"Index URL: {index_url}")
    return render_template('username.html')

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

# Store active games in memory (use a persistent store in production)
active_games = {}


@app.route('/start_game', methods=['POST'])
def start_game():
    username = request.json.get('username')  # Get the username from the request payload
    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        # Initialize the Kayttaja class to handle user
        user = Kayttaja()

        # Save or retrieve the user_id and username
        username, user_id = user.tallenna_kayttajatunnus(username)

        if not user_id:
            return jsonify({"error": "Could not find or create user"}), 500

        # Create a new game instance
        new_game = Peli(user_id, username)
        game_id = new_game.game_id

        # Store the game instance in active games
        active_games[game_id] = new_game

        # Save game_id in session for subsequent use
        session['game_id'] = game_id

        return jsonify({
            "message": "Game started",
            "game_id": game_id,
            "user_id": user_id  # Include the user_id in the response
        })
    except Exception as e:
        print(f"Error starting game: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_airports', methods=['GET'])
def get_airports():
    game_id = session.get('game_id')
    if not game_id or game_id not in active_games:
        return jsonify({"error": "No active game found"}), 400

    game = active_games[game_id]
    try:
        # Fetch the airport pair (ICAO codes)
        airport_pair = game.arvo_kentta()
        if not airport_pair or len(airport_pair) != 2:
            return jsonify({"error": "Could not generate airport pair"}), 500

        # Convert the set to a list for indexed access
        airport_pair = list(airport_pair)

        # Create Lentokentta objects for both airports
        airport1 = Lentokentta(airport_pair[0])
        airport2 = Lentokentta(airport_pair[1])

        # Check if data is complete for both airports
        if not airport1.korkeus or not airport2.korkeus:
            return jsonify({"error": "Missing elevation data for one or more airports"}), 500

        # Store the current airport pair in the session
        session['current_airports'] = {
            "airport1": {
                "ident": airport1.icao,
                "name": airport1.nimi,
                "elevation": airport1.korkeus,
            },
            "airport2": {
                "ident": airport2.icao,
                "name": airport2.nimi,
                "elevation": airport2.korkeus,
            },
        }

        # Return airport details
        return jsonify({
            "airport1": {
                "ident": airport1.icao,
                "name": airport1.nimi,
                "elevation": airport1.korkeus,
            },
            "airport2": {
                "ident": airport2.icao,
                "name": airport2.nimi,
                "elevation": airport2.korkeus,
            },
        })
    except Exception as e:
        print(f"Error fetching airports: {e}")
        return jsonify({"error": "Error fetching airports"}), 500


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'current_airports' not in session:
        return jsonify({'error': 'No airport pair available. Please try again.'})

    # Retrieve the saved airport pair
    current_airports = session['current_airports']
    airport1 = current_airports['airport1']
    airport2 = current_airports['airport2']

    # Get the user's choice from the request
    data = request.get_json()
    selected_airport = data.get('selected_airport')  # "1" or "2"

    # Determine the correct answer
    if airport1['elevation'] > airport2['elevation']:
        correct_answer = "1"
    else:
        correct_answer = "2"

    # Check if the user's choice is correct
    is_correct = (selected_airport == correct_answer)

    # Update score or any other game logic here
    score = session.get('score', 0)
    if is_correct:
        score += 1
    session['score'] = score

    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'score': score
    })


@app.route('/save_scores', methods=['POST'])
def save_scores():
    """Save the game's score to the database."""
    game_id = session.get('game_id')
    if not game_id or game_id not in active_games:
        return jsonify({"error": "No active game found"}), 400

    current_game = active_games[game_id]
    try:
        current_game.tallenna_pisteet()
        return jsonify({
            "message": f"Scores saved successfully for user {current_game.username}.",
            "score": current_game.pisteet
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
