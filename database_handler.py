import mysql.connector
from unidecode import unidecode


class DatabaseHandler:
    def __init__(self) -> None:
        # Constructor: opens the connection to the database.
        self.connection = mysql.connector.connect(
            host='localhost',
            user='unboard_admin',
            password='unboard_passwd',
            database='unboard'
        )
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        '''
        Closes the connection to the database.

        Returns None.
        '''
        self.cursor.close()
        self.connection.close()

    ###########################################################
    #           Create, Update and Delete functions           #
    ###########################################################

    def signup(self, email: str, name: str, password: str, profile_pic) -> bool:
        '''
        Register a new student on the database, given the parameters:
        email, name, password, profile picture

        Returns a bool indicating the success or failure of the operation.
        '''
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

    def login(self, email: str, password: str) -> bool:
        '''
        Checks if the login data is according to the data stored in the database,
        given the parameters: student email, student password.

        Returns a bool indicating the success or failure of the operation.
        '''
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

    def review_professor(self, student_email: str, prof_id: int, review: str) -> bool:
        '''
        Review a professor given the parameters: student email, professor id, review.

        Returns a bool indicating the success or failure of the operation.
        '''
        cmd = f'INSERT INTO ProfessorReviews VALUES ("{student_email}", {prof_id}, "{review}")'
        try:
            self.cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def review_class(self, student_email: str, class_id: int, review: str) -> bool:
        '''
        Review a class given the parameters: student email, class id, review.

        Returns a bool indicating the success or failure of the operation.
        '''
        cmd = f'INSERT INTO ClassReviews VALUES ("{student_email}", {class_id}, "{review}")'
        try:
            self.cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    ###########################################################
    #                      Read functions                     #
    ###########################################################

    def search_discipline(self, name: str) -> list:
        '''
        Gets disciplines with matching names with the search query.

        Returns a list, each item being a name that matches the query.
        '''
        query = f'SELECT name FROM Disciplines'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return
        entries = [i[0] for i in result if unidecode(name).lower() in unidecode(i[0]).lower()]
        return sorted(entries)

    def search_professor(self, name: str) -> list:
        '''
        Gets professors with matching names with the search query.

        Returns a list, each item being a tuple, each tuple being:
        (professor id, professor name)
        '''
        query = f'SELECT * FROM Professors'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return
        entries = [i for i in result if unidecode(name).lower() in unidecode(i[1]).lower()]
        return sorted(entries)

    def get_classes(self, discipline: str) -> list:
        '''
        Gets all classes that match the selected discipline.

        Returns a list of tuples, each tuple consisting of:
        (department name, department id,
        class id, class term, class code,
        professor name, professor id)
        '''
        query = f'SELECT D.name, D.id, C.id, C.term, C.code, P.name, P.id\
            FROM Professors AS P, Disciplines AS D, Classes AS C\
            WHERE P.id=C.prof_id AND D.id=C.disc_id AND D.name="{discipline}"'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_classreviews(self, id: int) -> list:
        '''
        Gets all reviews made for a class with a given id.

        Returns a list of tuples, each tuple consisting of: (student email, review text)
        '''
        query = f'SELECT student_email, review FROM ClassReviews WHERE class_id={id}'
        self.cursor.execute(query)
        query_result = [i for i in self.cursor.fetchall() if i]
        return query_result

    def get_professorreviews(self, id: int) -> list:
        '''
        Gets all reviews for a professor with a given id.

        Returns a list of tuples, each tuple consisting of: (student email, review text)
        '''
        query = f'SELECT student_email, review FROM ProfessorReviews WHERE prof_id={id}'
        self.cursor.execute(query)
        query_result = [i for i in self.cursor.fetchall() if i]
        return query_result
    
    def get_professorreviews_reports(self) -> list:
        '''
        Gets all professor reviews that were reported by students (users).

        Returns a list of tuples, each tuple consisting of: (student email, review text)
        '''
        query = f'SELECT PRR.student_email, PR.review\
            FROM ProfessorReviews AS PR, ProfessorReviewsReports AS PRR \
            WHERE PR.student_email=PRR.student_email AND PR.prof_id=PRR.prof_id'
        self.cursor.execute(query)
        query_result = [i for i in self.cursor.fetchall() if i]
        return query_result
    
    def get_classreviews_reports(self) -> list:
        '''
        Gets all class reviews that were reported by students (users).

        Returns a list of tuples, each tuple consisting of: (student email, review text)
        '''
        query = f'SELECT CRR.student_email, CR.review\
            FROM ClassReviews AS CR, ClassReviewsReports AS CRR \
            WHERE CR.student_email=CRR.student_email AND CR.class_id=CRR.class_id'
        self.cursor.execute(query)
        query_result = [i for i in self.cursor.fetchall() if i]
        return query_result

    def student_professor_reviews(self, email: str) -> list:
        '''
        Gets all professor reviews that a specific student made, given his email.

        Returns a list of tuples, each tuple consisting of: (professor name, review text)
        '''
        query = f'SELECT P.name, PR.review \
            FROM Professors AS P, ProfessorReviews AS PR \
            WHERE P.id=PR.prof_id AND PR.student_email="{email}"'
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        return query_result

    def student_class_reviews(self, email: str) -> list:
        '''
        Gets all class reviews that a specific student made, given his email.

        Returns a list of tuples, each tuple consisting of: 
        (class code, discipline name, term, professor name, class schedule, review text)
        '''
        query = f'SELECT C.code, D.name, C.term, P.name, C.schedule, CR.review\
            FROM Classes AS C, Disciplines as D, Professors as P, ClassReviews as CR\
            WHERE C.disc_id=D.id AND C.prof_id=P.id AND CR.class_id=C.id AND CR.student_email="{email}"'
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        return query_result

    def student_data(self, email: str) -> tuple:
        '''
        Gets stored data for a student.

        Returns a tuple consisting of: (student name, student profile picture)
        '''
        query = f'SELECT name, profile_pic FROM Students WHERE email="{email}"'
        self.cursor.execute(query)
        user = self.cursor.fetchall()[0]
        name, profile_pic = user
        return name, profile_pic
