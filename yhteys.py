import mysql.connector
# Yhdistäminen tietokantaan
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='root',
            password='kuha',
            autocommit=True
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Virhe yhteydessä MariaDB:hen: {e}")
        return None
