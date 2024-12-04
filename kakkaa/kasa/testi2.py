import mariadb

# aliohjelma joka luo listan vanhoista yhditelmistä joissa jokainen yhdistelmä on alkio
def vanhat_yhdistelmat():
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

        # SQL kysely
        haetaan_vanhat = """
            SELECT airport_ident1, airport_ident2
            FROM include;
        """

        # Suoritetaan kysely
        kursori.execute(haetaan_vanhat)

        # Haetaan tulokset
        haetut = kursori.fetchall()

        print(haetut) # Tulostetaan haetut tiedot

        vanhat = [] # lista vanhoille lentokentille, joihin lisätään alkioiksi joukkoja (koodiparit)

        for monikko in haetut:
            airport1, airport2 = monikko
            alkio_setti = {airport1, airport2}
            vanhat.append(alkio_setti) # Lisätään luodut joukot vanhat_listaan alkioon


    except mariadb.Error as err:
        print(f"Error: {err}")
        haetut = []  # Varmistetaan, että haetut on määritelty

    finally:
        # Suljetaan yhteys tietokantaan
        if yhteys:
            yhteys.close()
    return vanhat

print(vanhat_yhdistelmat())

