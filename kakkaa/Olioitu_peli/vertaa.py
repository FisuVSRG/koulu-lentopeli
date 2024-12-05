from kayttaja import Kayttaja
from peli import Peli

from kentta import Lentokentta

def vertaa_lentokenttien_korkeudet(peli):
    try:
        # Arvotaan lentokentät
        kentat = peli.arvo_kentta()
        # Jaetaan vastaus kahteen
        icao1, icao2 = kentat
        # luodaan oliot
        kentta1 = Lentokentta(icao1)
        kentta2 = Lentokentta(icao2)

        if kentta1.korkeus is None or kentta2.korkeus is None:
            print("Tietoja lentokenttien korkeuksista ei löytynyt.")
            return None
        return (("1", kentta1.korkeus, kentta2.korkeus)
                if kentta1.korkeus > kentta2.korkeus
                else ("2", kentta1.korkeus, kentta2.korkeus))
    except Exception as e:
        print(f"Virhe lentokenttien vertailussa: {e}")
        return None

def vastaus(peli):

    input("Tehtäväsi on valita kumpi kahdesta lentokentästä"
          " sijaitsee korkeammalla merenpinnasta"
          " \nPaina enter jatkaaksesi.")
    onko_oikein = None
    oikea_vastaus = vertaa_lentokenttien_korkeudet(peli)[0]
    if oikea_vastaus is None:
        print("Virhe vertailussa. Yritä uudelleen myöhemmin.")
        return False
    arvaus =  input("Valitse lentokentistä se, "
                    "joka sijaitsee korkeammalla merenpinnasta.")
    if arvaus == oikea_vastaus:
        print("Oikein")
        peli.lisaa_pisteita()
        onko_oikein = True
    else:
        print("Väärin")
        onko_oikein = False
    return onko_oikein
