import mariadb
import random

def arvo_kentta():  # pääaliohjelma joka kutsuu aiempaa
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
        # luodaan kursori
        kursori = yhteys.cursor()

        # SQL kysely jolla haetaan lentokenttien määrä
        sql_query = """
                    SELECT COUNT(*) FROM airport WHERE type = 'large_airport' 
                    AND iso_country IN ('DK', 'FI', 'IS', 'NO', 'SE');
                    """

        kursori.execute(sql_query)

        kenttien_maara = kursori.fetchone()[0]

        print(f"Number of rows in 'airport' table: {kenttien_maara}") # Tarkistetaan toimiko aiemmat kommennot


        #!#vanhat = vanhat_yhdistelmat()  # vanhat yhdistelmät toisesta aliohjelmasta

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

            # Suoritetaan satunnaisen lentokentän hakukysely
            kursori.execute(sql_kysely_random)
            icao = kursori.fetchone()[0]  # Haetaan ensimmäinen (ja ainoa) rivi ja sen ident-kenttä

            if icao not in yhdistelma:  # Estää sen että, sama lentokenttä tulisi kaksi kertaa pariin
                yhdistelma.add(icao)

            #!#if yhdistelma in vanhat and len(yhdistelma) == 2:  # jos joukko on vanhojenlistassa, poista jotta while luo uuden
                #!#yhdistelma.clear()

        # Puretaan joukko kahdeksi muuttujaksi
        icao_1, icao_2 = yhdistelma
        print(icao_1)
        print(icao_2)

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