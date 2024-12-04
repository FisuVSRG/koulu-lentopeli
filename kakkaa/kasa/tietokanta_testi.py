import mariadb
import random


# yhdistetään tietokantaan
yhteys = mariadb.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='pidätunkkisi',
    autocommit=True)


# aliohjelma joka luo listan vanhoista yhditelmistä joissa jokainen yhdistelmä on alkio

def vanhat_yhdistelmat():

    vanhat = [] # lista vanhoille lentokentille, joihin lisätään alkioiksi joukkoja (koodiparit)

    for rivi in include: # jokaista include-taulun riviä varten
        airport1 = rivi['airport_ident1']  # ICAO koodi 1 lentokentälle
        airport2 = rivi['airport_ident2']  # ICAO koodi 2 lentokentälle
        alkio_setti = {airport1, airport2}
        vanhat.append(alkio_setti) # Lisätään luodut joukot vanhat_listaan alkioon
    return vanhat



def arvo_kentta(): # pääaliohjelma joka kutsuu aiempaa
        kenttien_maara = 11
        yhdistelma = set() # tyhjä joukko yksittäistä lentokenttäparia varten
        vanhat = vanhat_yhdistelmat() # vanhat yhdistelmät toisesta aliohjelmasta

        while (len(yhdistelma)) < 2: # niin kaun kun joukossa on alle 2 alkiota
            icao = random.randint(0,kenttien_maara) # tähän pitää laittaa lentokentät
            if icao not in yhdistelma: # Estää sen että, sama lentokenttä tulisi kaksi kertaa pariin
                yhdistelma.add(icao)
            if yhdistelma in vanhat and len(yhdistelma) == 2: # jos joukko on vanhojenlistassa, poista jotta while luo uuden
                yhdistelma.clear()

        # Tähän joukon tallennus tietokantaan
        return yhdistelma # Palautetaan uniikki pari lentokenttiä

tulos = arvo_kentta()
print(tulos)

