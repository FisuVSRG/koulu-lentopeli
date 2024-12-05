
import random

vanhat = ({1,2},{2,3},{3,4},{4,5},{5,6},{6,7})



def arvo_lento(): # pääaliohjelma joka kutsuu aiempaa
        yhdistelma = set() # tyhjä joukko yksittäistä lentokenttäparia varten
        while (len(yhdistelma)) < 2: # niin kaun kun joukossa on alle 2 alkiota
            icao = (random.randint(0,11)) # tähän pitää laittaa lentokentät
            if icao not in yhdistelma: # Estää sen että, sama lentokenttä tulisi kaksi kertaa pariin
                yhdistelma.add(icao)
            if yhdistelma in vanhat and yhdistelma == 2: # jos joukko on vanhojenlistassa, poista jotta while luo uuden
                yhdistelma.clear()
        # Tähän joukon tallennus tietokantaan
        return yhdistelma # Palautetaan uniikki pari lentokenttiä

print(arvo_lento())