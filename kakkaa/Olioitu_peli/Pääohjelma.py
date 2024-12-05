from kayttaja import Kayttaja
from peli import Peli
from vertaa import vastaus
from tulostaulukko import tulostaulukko  # Lisää tämä import


def main():
    print("Tervetuloa Lentokenttä-haastepeliin!")
    print("Tehtävänäsi on arvata, kumpi lentokentistä sijaitsee korkeammalla merenpinnasta.\n")

    # Luo käyttäjä
    try:
        user = Kayttaja()
        print(f"Tervetuloa peliin, {user.username}!")
    except ConnectionError as e:
        print(f"Virhe tietokantayhteyden muodostamisessa: {e}")
        return

    # Luo uusi peli
    try:
        peli = Peli(user.user_id, user.username)
    except Exception as e:
        print(f"Virhe pelin alustamisessa: {e}")
        user.close_connection()
        return

    # Päävalikko
    while True:
        print("\n--- PÄÄVALIKKO ---")
        print("1. Pelaa peliä")
        print("2. Katso tulostaulukko")
        print("3. Lopeta peli")
        valinta = input("Valitse toiminto (1-3): ").strip()

        if valinta == "1":
            # Pelisilmukka
            pelaa = True
            while pelaa:
                print("\n--- UUSI KIERROS ---")
                oikein = vastaus(peli)
                if oikein is not None:  # Varmistaa, että kierros onnistui
                    print(f"Nykyiset pisteesi: {peli.pisteet}\n")

                # Tarkista haluaako käyttäjä jatkaa
                jatka = input("Haluatko pelata uudelleen? (k/e): ").strip().lower()
                if jatka != 'k':
                    pelaa = False

        elif valinta == "2":
            # Näytä tulostaulukko
            tulostaulukko(10)

        elif valinta == "3":
            # Päätetään peli
            try:
                peli.tallenna_pisteet()
                print(f"\nPeli päättyy. Keräsit yhteensä {peli.pisteet} pistettä.")
            except Exception as e:
                print(f"Virhe pisteiden tallentamisessa: {e}")

            # Sulje yhteydet
            peli.close_connection()
            user.close_connection()

            print("\nKiitos pelaamisesta! Näkemiin!")
            break
        else:
            print("Virheellinen valinta, yritä uudelleen.")
main()