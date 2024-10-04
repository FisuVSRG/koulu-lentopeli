import mariadb

yhteys = mariadb.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='pidätunkkisi',
         autocommit=True
         )