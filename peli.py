import mysql.connector
from mysql.connector import Error

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
        print(f"Virhe yhteydessä MariaDB:hen: {e}")
        return None

def check_user_exists(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] > 0  # Palauttaa True, jos tunnus löytyy
    except Error as e:
        print(f"Virhe käyttäjän tarkistuksessa: {e}")
        return False

def add_new_user(connection, username):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO user (username) VALUES (%s)"
        cursor.execute(query, (username,))
        connection.commit()  # Tallentaa muutokset tietokantaan
        print(f"Uusi käyttäjä {username} lisätty tietokantaan.")
    except Error as e:
        print(f"Virhe uuden käyttäjän lisäämisessä: {e}")
        connection.rollback()  # Peruuta muutokset virheen sattuessa

def tallenna_kayttajatunnus():
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

tila = 0

# Pelin päävalikko
while tila == 0:
    print("Tervetuloa pelaamaan!")
    print("1) Aloita peli")
    print("2) Tulostaulukko")
    print("3) Sulje ohjelma")
    aloitus = input("Aloita peli, katso korkeimmat tulokset tai sulje peli. \n")

# Tilan valinta ja pelin aloitus
    if aloitus == "1":
        tila = 1
        tallenna_kayttajatunnus()

# Tulostaulukko
    elif aloitus == "2":
        tila = 2
        while tila == 2:
            print()
# Lisää tähän funktio joka hakee korkeimmat tulokset järjestyksessä ja niiden käyttäjätunnukset.

# Ohjelman lopettaminen
    elif aloitus == "3":
        tila = 3
        break

# Virheellinen syöte
    else:
        print("Syöte on virheellinen. Anna syöte uudelleen.")

while tila == 1:
    print("Jatka ohjelmaa.")
    mielipide = input("Mielipide: ")