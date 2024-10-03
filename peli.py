import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='kuha',
         autocommit=True
         )

tila = 0

# Pelin päävalikko
while tila == 0:
    print("Tervetuloa pelaamaan!")
    print("1) Aloita peli")
    print("2) Tulostaulukko")
    print("3) Sulje ohjelma")
    aloitus = input("Valitse haluatko tehdä uuden käyttäjän vai jatkaa vanhalta. \n")

# Tilan valinta ja pelin aloitus
    if aloitus == "1":
        tila = 1
        tunnus = input("Syötä käyttäjätunnus: ")
        tallenna_kayttajatunnus(tunnus)

# Tulostaulukko
    elif aloitus == "2":
        tila = 1
# Lisää tähän funktio joka hakee korkeimmat tulokset järjestyksessä ja niiden käyttäjätunnukset.

# Ohjelman lopettaminen
    elif aloitus == "3":
        tila = 1
        break

# Virheellinen syöte
    else:
        print("Syöte on virheellinen. Anna syöte uudelleen.")

