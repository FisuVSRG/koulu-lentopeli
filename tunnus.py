import mysql.connector
from mysql.connector import Error

# Yhteyden luonti MariaDB-tietokantaan
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',          # MariaDB-palvelimen osoite
            user='root',               # MariaDB-käyttäjä
            password='2422',       # MariaDB-salasana
            database='kayttajatiedot'   # Tietokannan nimi
        )
        if connection.is_connected():
            print("Yhteys tietokantaan onnistui!")
        return connection
    except Error as e:
        print(f"Virhe: {e}")
        return None

# Funktio tunnuksen tallentamiseen
def tallenna_kayttajatunnus(tunnus):
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Tarkistetaan, onko käyttäjätunnus jo tietokannassa
        cursor.execute("SELECT tunnus FROM kayttajat WHERE tunnus = %s", (tunnus,))
        result = cursor.fetchone()

        if result:
            print("Käyttäjätunnus on jo käytössä. Valitse toinen tunnus.")
        else:
            # Jos tunnusta ei ole, lisätään se tietokantaan
            cursor.execute("INSERT INTO kayttajat (tunnus) VALUES (%s)", (tunnus,))
            connection.commit()
            print(f"Tervetuloa, {tunnus}!")

    except Error as e:
        print(f"Virhe: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Käyttäjätunnuksen syöttäminen
if __name__ == "__main__":
    tunnus = input("Syötä käyttäjätunnus: ")
    tallenna_kayttajatunnus(tunnus)
