import random
from pickle import FALSE
from wsgiref.util import request_uri

import mysql.connector
from mysql.connector import Error, connect

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
    except Error as e:
        print(f"Virhe uuden käyttäjän lisäämisessä: {e}")
        connection.rollback()  # Peruuta muutokset virheen sattuessa

def create_game_id(connection, user_id):
    try:
        cursor = connection.cursor()
        # Lisätään game_id game tauluun
        query = "INSERT INTO game (user_id) VALUES (%s)"  # Use %s instead of ?
        cursor.execute(query, (user_id,))
        connection.commit()
        game_id = cursor.lastrowid  # game_id uudelle pelille
        return game_id  # palauttaa game_id
    except Error as e:
        print(f"Virhe pelin ID:n luomisessa: {e}")
        connection.rollback()
        return None  # jos error niin none

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
        # haetaan olemassa oleva user id tässä
        user_id = get_user_id(connection, username)
    else:
        add_new_user(connection, username)
        print(f"Tervetuloa peliin, {username}!")
        user_id = get_user_id(connection, username)

    # luodaan uniikki game_id jokaiselle pelille
    game_id = create_game_id(connection, user_id)
    if game_id is not None:
        return game_id, username, user_id

    # Sulje yhteys tietokantaan
    if connection.is_connected():
        connection.close()

# aliohjelma joka luo listan vanhoista yhditelmistä joissa jokainen yhdistelmä on alkio
def vanhat_yhdistelmat(game_id):
    vanhat = []  # lista vanhoille lentokentille, joihin lisätään alkioiksi joukkoja (koodiparit)
    connection = connect_to_db()
    try:
        # Luodaan kursori
        kursori = connection.cursor()

        # SQL kysely lisää tähän vielä se että se ottaa oikeasta game_id:stä
        haetaan_vanhat = """
                SELECT airport_ident1, airport_ident2
                FROM include
                WHERE game_id = %s;
            """
        # Suoritetaan kysely
        kursori.execute(haetaan_vanhat, (game_id,))

        # Haetaan tulokset
        haetut = kursori.fetchall()
        for monikko in haetut:
            airport1, airport2 = monikko
            alkio_setti = {airport1, airport2}
            vanhat.append(alkio_setti)  # Lisätään luodut joukot vanhat_listaan alkioon

    except Error as err:
        print(f"Error: {err}")

    finally:  # suljetaan yhteys tietokantaan
        if connection:
            connection.close()

    return vanhat

def arvo_kentta(game_id):  # pääaliohjelma joka kutsuu aiempaa KUTSU TÄTÄ, saa parametriksi game_id
    yhdistelma = set()  # tyhjä joukko yksittäistä lentokenttäparia varten
    connection = connect_to_db()

    try:
        kursori = connection.cursor()  # luodaan kursori
        # SQL kysely jolla haetaan lentokenttien määrä
        sql_query = """
                        SELECT COUNT(*) FROM airport WHERE type = 'large_airport' 
                        AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE');
                        """
        kursori.execute(sql_query)
        kenttien_maara = kursori.fetchone()[0]

        vanhat = vanhat_yhdistelmat(game_id)  # vanhat yhdistelmät toisesta aliohjelmasta

        while (len(yhdistelma)) < 2:  # niin kaun kun joukossa on alle 2 alkiota
            rivi_offset = random.randint(1, kenttien_maara - 1)  # kuinka monta riviä skipataan

            # SQL kysely jolla haetaan lentokenttä ident kentän avulla satunnaisen rivin perusteella
            sql_kysely_random = """
                               SELECT ident 
                               FROM airport 
                               WHERE type = 'large_airport' 
                               AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE') 
                               LIMIT 1 OFFSET %s;
                           """ % rivi_offset
            kursori.execute(sql_kysely_random)
            icao = kursori.fetchone()[0]  # Haetaan ensimmäinen (ja ainoa) rivi ja sen ident-kenttä

            if icao not in yhdistelma:  # Estää sen että, sama lentokenttä tulisi kaksi kertaa yhdistelmään
                yhdistelma.add(icao)  # Lisätään icao yhdistelmään

            if yhdistelma in vanhat and len(yhdistelma) == 2:  # jos joukko on vanhojenlistassa, poista jotta while luo uuden
                yhdistelma.clear()

        # Puretaan joukko kahdeksi muuttujaksi
        icao_1, icao_2 = yhdistelma

        # Lisätään yhdistelmä include-tauluun
        insert_query = """
                                 INSERT INTO include (airport_ident1, airport_ident2,game_ID)
                                 VALUES (%s, %s, %s);
                                 WHERE game_id = %s;
                                 """
        kursori.execute(insert_query,
                        (icao_1, icao_2, game_id, game_id,))

    except Error as err:
        print(f"Error: {err}")

    finally:  # suljetaan yhteys tietokantaan
        if connection:
            connection.close()

    return yhdistelma  # palauttaa kaksi uniikkia ICAO-koodia joukkona


# Funktio hakee lentokentän korkeuden jalkoina
def hae_korkeus(icao, connection):
    try:
        cursor = connection.cursor()
        query = "SELECT elevation_ft FROM airport WHERE ident = %s"
        cursor.execute(query, (icao,))
        tulos = cursor.fetchone()

        if tulos:
            korkeus_jalat = tulos[0]
            korkeus_metrit = korkeus_jalat * 0.3048  # Muunnos jalkoina metreiksi
            return korkeus_metrit
        else:
            print(f"Lentokenttää koodilla {icao} ei löytynyt.")
            return None
    except Error as e:
        print(f"Virhe tietoa haettaessa: {e}")
        return None


# Funktio, joka vertailee kahden lentokentän korkeudet
def vertaa_lentokenttien_korkeudet(icao1, icao2):
    connection = connect_to_db()

    if connection:
        # Hae korkeudet
        korkeus1 = hae_korkeus(icao1, connection)
        korkeus2 = hae_korkeus(icao2, connection)

        # Sulje tietokantayhteys
        connection.close()

        if korkeus1 is None or korkeus2 is None:
            return None

        # Vertaile korkeuksia ja palauta korkeammalla olevan kentän numero (1 tai 2)
        if korkeus1 > korkeus2:
            return "1", korkeus1, korkeus2
        else:
            return "2", korkeus1, korkeus2
    else:
        return None

def tallenna_pisteet(username, user_id, pisteet, game_id):

    connection = connect_to_db()

    if connection.is_connected():
        cursor = connection.cursor()

         # Lisätään pisteet käyttäjän ID:llä
        sql_lause = "INSERT INTO game (user_id, score) VALUES (%s, %s)"
        cursor.execute(sql_lause, (user_id, pisteet,))

        # Tallennetaan muutokset
        connection.commit()

        print(f"Pisteet tallennettu käyttäjälle: {username}, pisteet: {pisteet}")

# Funktio, jolla luodaan 10 parhaan pelin tulostaulukko.
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

        # Tulostetaan parhaat 10 tulosta, ja jätetään pois ne, jotka ovat tyhjiä.
        for i in parhaat:
            nimi, score = i
            score_str = str(score)

            if "None" not in score_str:
                print(i)

# Funktio joka hakee lentokentän nimen sen ICAO-koodin perusteella
def lentokentan_nimi(icao):
    connection = connect_to_db()

    if connection.is_connected():
        cursor = connection.cursor()
        nimenhaku = "SELECT name FROM airport WHERE ident = %s"
        cursor.execute(nimenhaku, (icao,))
        name = cursor.fetchone()[0]
        return name

tila = 0
arvaus = ""
pisteet = 0


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
        game_id, username, user_id = tallenna_kayttajatunnus()

# Tulostaulukko
    elif aloitus == "2":
        tila = 2
        while tila == 2:
            # Lisää tähän funktio joka hakee korkeimmat tulokset järjestyksessä ja niiden käyttäjätunnukset.
            print("Nimi | Tulos")
            tulostaulukko()
            input("Paina enter päästäksesi takaisin päävalikkoon.")
            tila = 0

# Ohjelman lopettaminen
    elif aloitus == "3":
        tila = 3
        break

# Virheellinen syöte
    else:
        print("Syöte on virheellinen. Anna syöte uudelleen.")

# Ohjelman jatkaminen kun peli alkaa.
while tila == 1:
    # Silmukka, joka kysyy pelaajalta 10 kertaa korkeammalla
    for i in range(1, 11):
        icao1, icao2 = arvo_kentta(game_id)
        oikein, korkeus1, korkeus2 = vertaa_lentokenttien_korkeudet(icao1, icao2)
        nimi1 = lentokentan_nimi(icao1)
        nimi2 = lentokentan_nimi(icao2)
        print(f"1. {nimi1}")
        print(f"2. {nimi2}")
        while arvaus != "1" and arvaus != "2":
            arvaus = input("Valitse lentokentistä korkeammalla oleva.")
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

# vittu mä hirtän itteni tänään