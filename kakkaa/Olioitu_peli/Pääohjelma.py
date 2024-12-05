from kayttaja import Kayttaja
from peli import Peli
from kentta import Lentokentta

if __name__ == "__main__":
    try:
        # Luo käyttäjä-olio
        kayttaja = Kayttaja()

        # Luo peli-olio käyttäjän ID:n perusteella
        if kayttaja.user_id:
            peli = Peli(kayttaja.user_id)
            print(f"Uusi peli luotu käyttäjälle {kayttaja.username}. Peli-ID: {peli.game_id}")

            # Arvotaan lentokentät
            kentat = peli.arvo_kentta() # tätä kutsutaan coreloopissa.
            # Jaetaan vastaus kahteen
            icao1, icao2 = kentat
            # luodaan oliot
            kentta1 = Lentokentta(icao1)
            kentta2 = Lentokentta(icao2)
            print(f"Arvotut lentokentät: {kentat}")
            print(f"Kentän {icao1} nimi on: {kentta1.nimi}")
            print(f"Kentän {icao2} nimi on: {kentta2.nimi}")

        else:
            print("Käyttäjän ID:tä ei voitu määrittää.")
    except Exception as e:
        print(f"Tapahtui virhe: {e}")
    finally:
        # Suljetaan yhteydet
        if 'peli' in locals():
            peli.close_connection()
        if 'kayttaja' in locals():
            kayttaja.close_connection()
