import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        # Yhdistä MariaDB-tietokantaan
        connection = mysql.connector.connect(
            host='localhost',         # Muuta tarvittaessa
            database='kayttajat_db',   # Tietokanta, jossa on käyttäjätiedot
            user='root',               # Muuta tarvittaessa
            password='2422'        # Muuta tarvittaessa
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Virhe yhteydessä MariaDB:hen: {e}")
        return None

def check_user_exists(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM kayttajat WHERE tunnus = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] > 0  # Palauttaa True, jos tunnus löytyy
    except Error as e:
        print(f"Virhe käyttäjän tarkistuksessa: {e}")
        return False

def add_new_user(connection, username):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO kayttajat (tunnus) VALUES (%s)"
        cursor.execute(query, (username,))
        connection.commit()  # Tallentaa muutokset tietokantaan
        print(f"Uusi käyttäjä {username} lisätty tietokantaan.")
    except Error as e:
        print(f"Virhe uuden käyttäjän lisäämisessä: {e}")
        connection.rollback()  # Peruuta muutokset virheen sattuessa

def main():
    # Yhdistä tietokantaan
    connection = connect_to_db()
    if connection is None:
        return

    # Kysy käyttäjätunnusta
    username = input("Anna käyttäjätunnus: ")

    # Tarkista, onko käyttäjätunnus jo olemassa
    if check_user_exists(connection, username):
        print(f"Tervetuloa takaisin, {username}!")
    else:
        add_new_user(connection, username)
        print(f"Tervetuloa, uusi käyttäjä {username}!")

    # Sulje yhteys tietokantaan
    if connection.is_connected():
        connection.close()


if __name__ == "__main__":
    main()
