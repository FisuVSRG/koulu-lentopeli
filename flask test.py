from flask import Flask, render_template, request, jsonify
from mysql.connector import Error
import mysql.connector
from flask_cors import CORS

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


@app.route('/check_username', methods=['POST'])
def check_username():
    print("Received POST request on /check_username")
    username = request.form.get('username')
    print(f"Received username: {username}")

    if not username:
        return jsonify({'status': 'error', 'message': 'Username not provided'})

    connection = connect_to_db()
    if connection is None:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})

    if check_user_exists(connection, username):
        user_id = get_user_id(connection, username)
        message = f"Welcome back, {username}!"
    else:
        add_new_user(connection, username)
        user_id = get_user_id(connection, username)
        message = f"Welcome to the game, {username}!"

    game_id = create_game_id(connection, user_id)
    if game_id is not None:
        response = {'status': 'success', 'message': message, 'game_id': game_id, 'user_id': user_id}
    else:
        response = {'status': 'error', 'message': 'Failed to create game ID'}

    if connection.is_connected():
        connection.close()

    print(f"Response: {response}")
    return jsonify(response)


@app.route('/top-scores')
def top_scores():
    scores = tulostaulukko()
    return render_template('top_scores.html', scores=scores)


@app.route('/api/top-scores')
def api_top_scores():
    scores = tulostaulukko()
    return jsonify(scores)


def connect_to_db():
    try:
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
        print(f"Error connecting to MySQL: {e}")
        return None


def check_user_exists(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] > 0
    except Error as e:
        print(f"Error checking user: {e}")
        return False


def add_new_user(connection, username):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO user (username) VALUES (%s)"
        cursor.execute(query, (username,))
        connection.commit()
    except Error as e:
        print(f"Error adding new user: {e}")
        connection.rollback()


def create_game_id(connection, user_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO game (user_id) VALUES (%s)"
        cursor.execute(query, (user_id,))
        connection.commit()
        game_id = cursor.lastrowid
        return game_id
    except Error as e:
        print(f"Error creating game ID: {e}")
        connection.rollback()
        return None


def get_user_id(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT ID FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"Error fetching user ID: {e}")
        return None


def tulostaulukko():
    connection = connect_to_db()
    if connection.is_connected():
        cursor = connection.cursor()
        tulokset = """SELECT username, score
                      FROM user
                      INNER JOIN game ON game.user_id = user.id
                      ORDER BY score DESC
                      LIMIT 10"""
        cursor.execute(tulokset)
        parhaat = cursor.fetchall()
        results = [{"username": nimi, "score": score} for nimi, score in parhaat if score is not None]
        return results


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
