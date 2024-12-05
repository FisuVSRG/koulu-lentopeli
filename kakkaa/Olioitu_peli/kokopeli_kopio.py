import random
import mariadb


def connect_to_db():
    try:
        connection = mariadb.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='root',
            password='pidätunkkisi',
            autocommit=True
        )
        return connection
    except mariadb.Error as e:
        print(f"Virhe yhteydessä MariaDB:hen: {e}")
        return None


def check_user_exists(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] > 0
    except mariadb.Error as e:
        print(f"Virhe käyttäjän tarkistuksessa: {e}")
        return False


def add_new_user(connection, username):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO user (username) VALUES (?)"
        cursor.execute(query, (username,))
    except mariadb.Error as e:
        print(f"Virhe uuden käyttäjän lisäämisessä: {e}")
        connection.rollback()


def get_user_id(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT id FROM user WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except mariadb.Error as e:
        print(f"Virhe käyttäjän ID:n hakemisessa: {e}")
        return None


def create_game_id(connection, user_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO game (user_id) VALUES (?)"
        cursor.execute(query, (user_id,))
        game_id = cursor.lastrowid
        return game_id
    except mariadb.Error as e:
        print(f"Virhe pelin ID:n luomisessa: {e}")
        connection.rollback()
        return None


def tallenna_kayttajatunnus():
    connection = connect_to_db()
    if connection is None:
        return None, None, None

    try:
        username = input("Anna käyttäjätunnus: ")
        if check_user_exists(connection, username):
            print(f"Tervetuloa takaisin, {username}!")
            user_id = get_user_id(connection, username)
        else:
            add_new_user(connection, username)
            print(f"Tervetuloa peliin, {username}!")
            user_id = get_user_id(connection, username)

        game_id = create_game_id(connection, user_id)
        if game_id is not None:
            return game_id, username, user_id
    except mariadb.Error as e:
        print(f"Virhe käyttäjätunnuksen tallentamisessa: {e}")
    finally:
        if connection:
            connection.close()


def vanhat_yhdistelmat(game_id):
    vanhat = []
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        query = """
            SELECT airport_ident1, airport_ident2
            FROM include
            WHERE game_id = ?;
        """
        cursor.execute(query, (game_id,))
        haetut = cursor.fetchall()
        for monikko in haetut:
            vanhat.append(set(monikko))
    except mariadb.Error as err:
        print(f"Virhe vanhojen yhdistelmien haussa: {err}")
    finally:
        if connection:
            connection.close()
    return vanhat


def arvo_kentta(game_id):
    yhdistelma = set()
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        query_count = """
            SELECT COUNT(*) FROM airport
            WHERE type = 'large_airport' AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE');
        """
        cursor.execute(query_count)
        kenttien_maara = cursor.fetchone()[0]
        vanhat = vanhat_yhdistelmat(game_id)

        while len(yhdistelma) < 2:
            rivi_offset = random.randint(1, kenttien_maara - 1)
            query_random = """
                SELECT ident FROM airport
                WHERE type = 'large_airport' AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE')
                LIMIT 1 OFFSET ?;
            """
            cursor.execute(query_random, (rivi_offset,))
            icao = cursor.fetchone()[0]
            if icao not in yhdistelma:
                yhdistelma.add(icao)

            if yhdistelma in vanhat and len(yhdistelma) == 2:
                yhdistelma.clear()

        icao_1, icao_2 = yhdistelma
        query_insert = """
            INSERT INTO include (airport_ident1, airport_ident2, game_id)
            VALUES (?, ?, ?);
        """
        cursor.execute(query_insert, (icao_1, icao_2, game_id))
        connection.commit()
    except mariadb.Error as err:
        print(f"Virhe lentokentän arvonnassa: {err}")
    finally:
        if connection:
            connection.close()
    return yhdistelma


def hae_korkeus(icao, connection):
    try:
        cursor = connection.cursor()
        query = "SELECT elevation_ft FROM airport WHERE ident = ?"
        cursor.execute(query, (icao,))
        result = cursor.fetchone()
        if result:
            return result[0] * 0.3048  # Muunna metreiksi
        else:
            print(f"Lentokenttää koodilla {icao} ei löytynyt.")
            return None
    except mariadb.Error as e:
        print(f"Virhe lentokentän korkeuden haussa: {e}")
        return None


def vertaa_lentokenttien_korkeudet(icao1, icao2):
    connection = connect_to_db()
    if connection:
        korkeus1 = hae_korkeus(icao1, connection)
        korkeus2 = hae_korkeus(icao2, connection)
        connection.close()
        if korkeus1 is None or korkeus2 is None:
            return None
        return ("1", korkeus1, korkeus2) if korkeus1 > korkeus2 else ("2", korkeus1, korkeus2)
    return None

def tallenna_pisteet(username, user_id, pisteet, game_id):
    connection = connect_to_db()
    if connection is None:
        print("Yhteys tietokantaan epäonnistui.")
        return

    try:
        cursor = connection.cursor()

        # Päivitetään pisteet pelin ID:llä
        sql_lause = "UPDATE game SET score = ? WHERE id = ? AND user_id = ?"
        cursor.execute(sql_lause, (pisteet, game_id, user_id))
        connection.commit()

        print(f"Pisteet tallennettu käyttäjälle: {username}, pisteet: {pisteet}")
    except mariadb.Error as e:
        print(f"Virhe pisteiden tallentamisessa: {e}")
        connection.rollback()
    finally:
        if connection:
            connection.close()


def tulostaulukko():
    connection = connect_to_db()
    if connection is None:
        print("Yhteys tietokantaan epäonnistui.")
        return

    try:
        cursor = connection.cursor()

        # Haetaan parhaat 10 tulosta
        tulokset = """
            SELECT user.username, game.score
            FROM user
            INNER JOIN game ON game.user_id = user.id
            WHERE game.score IS NOT NULL
            ORDER BY game.score DESC
            LIMIT 10
        """
        cursor.execute(tulokset)
        parhaat = cursor.fetchall()

        # Tulostetaan parhaat tulokset
        print("TOP 10 PELAAJAA:")
        for i, (nimi, score) in enumerate(parhaat, 1):
            print(f"{i}. {nimi}: {score} pistettä")
    except mariadb.Error as e:
        print(f"Virhe tulostaulukon hakemisessa: {e}")
    finally:
        if connection:
            connection.close()



def lentokentan_nimi(icao):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        query = "SELECT name FROM airport WHERE ident = ?"
        cursor.execute(query, (icao,))
        result = cursor.fetchone()
        return result[0] if result else None
    except mariadb.Error as e:
        print(f"Virhe lentokentän nimen haussa: {e}")
        return None
    finally:
        if connection:
            connection.close()
tila = 0
arvaus = ""
pisteet = 0


# Pelin päävalikko
while tila == 0:
    input("Tervetuloa pelaamaan! Paina enter jatkaaksesi.")
    print("1) Aloita peli")
    print("2) Tulostaulukko")
    print("3) Sulje ohjelma")
    aloitus = input("Aloita peli, katso korkeimmat tulokset tai sulje peli.")

# Tilan valinta ja pelin aloitus
    if aloitus == "1":
        tila = 1
        game_id, username, user_id = tallenna_kayttajatunnus()

# Tulostaulukko
    elif aloitus == "2":
        tila = 2
        while tila == 2:
            # Tähän funktio joka hakee korkeimmat tulokset järjestyksessä ja niiden käyttäjätunnukset.
            print("Nimi | Tulos")
            tulostaulukko()
            input("Paina enter päästäksesi takaisin päävalikkoon.")
            tila = 0

# Ohjelman lopettaminen
    elif aloitus == "3":
        print("Nähdään ensi kerralla!")
        tila = 3
        break

# Virheellinen syöte
    else:
        print("Syöte on virheellinen. Anna syöte uudelleen.")

# Ohjelman jatkaminen kun peli alkaa.
while tila == 1:
    input("Tehtäväsi on valita kumpi kahdesta lentokentästä sijaitsee korkeammalla merenpinnasta \nPaina enter jatkaaksesi.")
    # Silmukka, joka kysyy pelaajalta 10 kertaa korkeammalla
    for i in range(1, 11):
        icao1, icao2 = arvo_kentta(game_id)
        oikein, korkeus1, korkeus2 = vertaa_lentokenttien_korkeudet(icao1, icao2)
        nimi1 = lentokentan_nimi(icao1)
        nimi2 = lentokentan_nimi(icao2)
        print(f"1. {nimi1}")
        print(f"2. {nimi2}")

        while arvaus != "1" and arvaus != "2":
            arvaus = input("Valitse lentokentistä se, joka sijaitsee korkeammalla merenpinnasta.")
            if arvaus != "1" and arvaus != "2":
                print("Virheellinen syöte.")
            elif arvaus == oikein and arvaus == "1":
                pisteet = pisteet + 100
                print(f"Oikein! Valitsit {nimi1}, sen korkeus on {korkeus1: .2f}m")
            elif arvaus == oikein and arvaus == "2":
                pisteet = pisteet + 100
                print(f"Oikein! Valitsit {nimi2}, sen korkeus on {korkeus2: .2f}m")
            elif arvaus != oikein and arvaus == "1":
                pisteet = pisteet
                print(f"Väärin. Valitsit {nimi1}, sen korkeus on {korkeus1: .2f}m")
            elif arvaus != oikein and arvaus == "2":
                pisteet = pisteet
                print(f"Väärin. Valitsit {nimi2}, sen korkeus on {korkeus2: .2f}m")
        arvaus = ""
    print(f"{pisteet}")
    tallenna_pisteet(username, user_id, pisteet, game_id)
    print("Kiitos pelaamisesta!!!")
    tila = 2
print(game_id)
print(user_id)