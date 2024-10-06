import mysql.connector
from mysql.connector import Error

def tallenna_pisteet(käyttäjänimi, pisteet):
    try:
        # Yhdistä tietokantaan
        yhteys = mysql.connector.connect(
            host='localhost',
            database='pelit',
            user='root',
            password='salasana'
        )

        if yhteys.is_connected():
            cursor = yhteys.cursor()

            # Tarkistetaan, onko käyttäjä olemassa
            cursor.execute("SELECT id FROM käyttäjät WHERE käyttäjänimi = %s", (käyttäjänimi,))
            tulos = cursor.fetchone()

            if tulos:
                käyttäjä_id = tulos[0]
            else:
                # Lisätään uusi käyttäjä, jos ei ole vielä olemassa
                cursor.execute("INSERT INTO käyttäjät (käyttäjänimi) VALUES (%s)", (käyttäjänimi,))
                yhteys.commit()
                käyttäjä_id = cursor.lastrowid  # Haetaan juuri lisätyn käyttäjän ID

            # Lisätään pisteet käyttäjän ID:llä
            sql_lause = "INSERT INTO pelin_pisteet (käyttäjä_id, pisteet) VALUES (%s, %s)"
            cursor.execute(sql_lause, (käyttäjä_id, pisteet))

            # Tallennetaan muutokset
            yhteys.commit()

            print(f"Pisteet tallennettu käyttäjälle: {käyttäjänimi}, pisteet: {pisteet}")

    except Error as e:
        print(f"Virhe yhteydessä MySQL-tietokantaan: {e}")

    finally:
        if yhteys.is_connected():
            cursor.close()
            yhteys.close()

