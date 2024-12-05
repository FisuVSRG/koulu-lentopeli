import mariadb
from yhteys import connect_to_db

def tulostaulukko(top_mika):
    connection = connect_to_db()
    if connection is None:
        print("Yhteys tietokantaan epäonnistui.")
        return

    try:
        cursor = connection.cursor()

        # Parametrisoitu kysely ilman suoraa LIMIT-parametria
        tulokset = f"""
            SELECT user.username, game.score
            FROM user
            INNER JOIN game ON game.user_id = user.id
            WHERE game.score IS NOT NULL
            ORDER BY game.score DESC
            LIMIT {top_mika}
        """
        cursor.execute(tulokset)
        parhaat = cursor.fetchall()

        # Tulostetaan parhaat tulokset
        print(f"TOP {top_mika} PELAAJAA:")
        for i, (nimi, score) in enumerate(parhaat, 1):
            print(f"{i}. {nimi}: {score} pistettä")
    except mariadb.Error as e:
        print(f"Virhe tulostaulukon hakemisessa: {e}")
    finally:
        if connection:
            connection.close()
