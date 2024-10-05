import mariadb
import random

# Loin tietokantaan game_id arvolla 1 (INSERT INTO game (ID, Score) VALUES (1, 0);) noin rivi 100

# aliohjelma joka luo listan vanhoista yhditelmistä joissa jokainen yhdistelmä on alkio
def vanhat_yhdistelmat(game_id):
    vanhat = []  # lista vanhoille lentokentille, joihin lisätään alkioiksi joukkoja (koodiparit)
    # Yhdistetään tietokantaan
    yhteys = mariadb.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='root',
        password='pidätunkkisi',
        autocommit=True)

    try:
        # Luodaan kursori
        kursori = yhteys.cursor()

        # SQL kysely lisää tähän vielä se että se ottaa oikeasta game_id:stä
        haetaan_vanhat = """
            SELECT airport_ident1, airport_ident2
            FROM include;
        """
        # Suoritetaan kysely
        kursori.execute(haetaan_vanhat)

        # Haetaan tulokset
        haetut = kursori.fetchall()
        for monikko in haetut:
            airport1, airport2 = monikko
            alkio_setti = {airport1, airport2}
            vanhat.append(alkio_setti) # Lisätään luodut joukot vanhat_listaan alkioon

    except mariadb.Error as err:
        print(f"Error: {err}")

    finally:
        # Suljetaan yhteys tietokantaan
        if yhteys:
            yhteys.close()
    return vanhat

print(vanhat_yhdistelmat())

def arvo_kentta(game_id):  # pääaliohjelma joka kutsuu aiempaa KUTSU TÄTÄ, saa parametriksi game_id
    yhdistelma = set()  # tyhjä joukko yksittäistä lentokenttäparia varten
    # yhdistetään tietokantaan
    yhteys = mariadb.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='root',
        password='pidätunkkisi',
        autocommit=True)

    try:
        kursori = yhteys.cursor() # luodaan kursori
        # SQL kysely jolla haetaan lentokenttien määrä
        sql_query = """
                    SELECT COUNT(*) FROM airport WHERE type = 'large_airport' 
                    AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE');
                    """
        kursori.execute(sql_query)
        kenttien_maara = kursori.fetchone()[0]

        vanhat = vanhat_yhdistelmat()  # vanhat yhdistelmät toisesta aliohjelmasta

        while (len(yhdistelma)) < 2:  # niin kaun kun joukossa on alle 2 alkiota
            rivi_offset = random.randint(1, kenttien_maara-1)  # kuinka monta riviä skipataan

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
                yhdistelma.add(icao) # Lisätään icao yhdistelmään

            if yhdistelma in vanhat and len(yhdistelma) == 2:  # jos joukko on vanhojenlistassa, poista jotta while luo uuden
                print(f"luotu yhdistelma{yhdistelma}")
                yhdistelma.clear()
                print("yhdistelmä jo käytössä luodaan uusi")

        # Puretaan joukko kahdeksi muuttujaksi
        icao_1, icao_2 = yhdistelma

        game_id = 1 # Kokeilemista varten oleva game ID, korvaa myöhemmin!!!!!

        # Lisätään yhdistelmä include-tauluun
        insert_query = """
                             INSERT INTO include (airport_ident1, airport_ident2,game_ID)
                             VALUES (?, ?, ?);
                             """
        kursori.execute(insert_query, (icao_1, icao_2, game_id)) # Kokeilemista varten oleva game ID, korvaa myöhemmin!!!!!
        print(f"Tallennettu: {icao_1} ja {icao_2}")

    except mariadb.Error as err:
        print(f"Error: {err}")

    finally: # suljetaan yhteys tietokantaan
        if yhteys:
            yhteys.close()

    return yhdistelma  # palauttaa kaksi uniikkia ICAO-koodia joukkona

print(arvo_kentta())