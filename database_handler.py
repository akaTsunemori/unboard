import mysql.connector


class DatabaseHandler:
    def __init__(self) -> None:
        # Abrir conexao e cursor
        self.connection = mysql.connector.connect(
            host='localhost',
            user='unboard_admin',
            password='unboard_admin',
            database='unboard'
        )
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    #####################
    #   CRUD Functions  #
    #####################

    def signup():
        pass

    def login():
        pass

    #####################
    #  Query Functions  #
    #####################

    def search():
        pass
