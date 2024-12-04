import mysql.connector  # Change import to MySQL Connector
from mysql.connector import Error  # Update import to match MySQL Connector

def connect_to_db():
    try:
        # Yhdistä MySQL-tietokantaan
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='root',
            password='pidätunkkisi',
            autocommit=True
        )
        return connection
    except Error as e:
        print(f"Virhe yhteydessä MySQL:hen: {e}")
        return None

def check_user_exists(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = %s"  # Use %s instead of ?
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] > 0  # Palauttaa True, jos tunnus löytyy
    except Error as e:
        print(f"Virhe käyttäjän tarkistuksessa: {e}")
        return False

def add_new_user(connection, username):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO user (username) VALUES (%s)"  # Use %s instead of ?
        cursor.execute(query, (username,))
        connection.commit()  # Tallentaa muutokset tietokantaan
        print(f"Uusi käyttäjä {username} lisätty tietokantaan.")
        return cursor.lastrowid  # Return the ID of the new user
    except Error as e:
        print(f"Virhe uuden käyttäjän lisäämisessä: {e}")
        connection.rollback()  # Peruuta muutokset virheen sattuessa
        return None  # palauttaa None jos error

def create_game_id(connection, user_id):
    try:
        cursor = connection.cursor()
        # Lisätään game_id game tauluun
        query = "INSERT INTO game (user_id) VALUES (%s)"  # Use %s instead of ?
        cursor.execute(query, (user_id,))
        connection.commit()
        game_id = cursor.lastrowid  # game_id uudelle pelille
        print(f"Uusi peli luotu, peli-ID: {game_id}")
        return game_id  # palauttaa game_id
    except Error as e:
        print(f"Virhe pelin ID:n luomisessa: {e}")
        connection.rollback()
        return None  # jos error niin none

def main():
    # Yhdistä tietokantaan
    connection = connect_to_db()
    if connection is None:
        return

    # Kysy käyttäjätunnusta
    username = input("Anna käyttäjätunnus: ")

    # Tarkista, onko käyttäjätunnus jo olemassa
    user_id = None  # alustetaan user_id noneksi
    if check_user_exists(connection, username):
        print(f"Tervetuloa takaisin, {username}!")
        # haetaan olemassa oleva user id tässä
        user_id = get_user_id(connection, username)
    else:
        user_id = add_new_user(connection, username)
        print(f"Tervetuloa, uusi käyttäjä {username}!")

    # luodaan uniikki game_id jokaiselle pelille
    game_id = create_game_id(connection, user_id)
    if game_id is not None:
        print(f"Pelin ID on: {game_id}")

    # Sulje yhteys tietokantaan
    if connection:
        connection.close()

def get_user_id(connection, username):
    """ Fetches the user ID for an existing username. """
    try:
        cursor = connection.cursor()
        query = "SELECT ID FROM user WHERE username = %s"  # Use %s instead of ?
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None  # palauttaa user idn jos löytyy
    except Error as e:
        print(f"Virhe käyttäjän ID:n hakemisessa: {e}")
        return None

if __name__ == "__main__":
    main()
