import mysql.connector


class DatabaseHandler:
    def __init__(self) -> None:
        # Abrir conexao e cursor
        self.connection = mysql.connector.connect(
            host='localhost',
            user='unboard_admin',
            password='unboard_passwd',
            database='unboard'
        )
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    #####################
    #   CRUD Functions  #
    #####################

    def signup(self, email: str, name: str, password: str, profile_pic) -> bool:
        check_email = f'SELECT * FROM Students WHERE email="{email}"'
        self.cursor.execute(check_email)
        exists_email = self.cursor.fetchall()
        if exists_email:
            return False
        profile_pic_data = profile_pic.read()
        cmd = f'INSERT INTO Students (email, name, passwd, profile_pic) \
                VALUES ("{email}", "{name}", "{password}", _binary %s)'
        self.cursor.execute(cmd, (profile_pic_data,))
        self.connection.commit()
        return True

    def login(self, email: str, password: str):
        select_user = f'SELECT * FROM Students WHERE email="{email}"'
        self.cursor.execute(select_user)
        user = self.cursor.fetchall()
        if not user:
            return False
        user = user[0]
        db_password = user[2]
        if password != db_password:
            return False
        return True

    #####################
    #  Query Functions  #
    #####################

    def search(self, term: str):
        query = f'SELECT name FROM Disciplines'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return
        entries = [i[0] for i in result if term.lower() in i[0].lower()]
        return entries

    def student_data(self, email: str):
        query = f'SELECT name, profile_pic FROM Students WHERE email="{email}"'
        self.cursor.execute(query)
        user = self.cursor.fetchall()[0]
        name, profile_pic = user
        return name, profile_pic
