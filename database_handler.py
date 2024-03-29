import mysql.connector
from unidecode import unidecode


class DatabaseHandler:
    '''
    This is the main handler for the communitcation between the application and
    the MySQL database. Every query is explicit and every function is well documented.

    The unidecode module is used in order to make a better comparison of strings
    when searching, for example, 'Lélio' and 'LELio' should be considered equal.
    '''
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

    def signup(self, email: str, name: str, password: str, is_admin: bool, course: str, id: int, profile_pic) -> bool:
        '''
        Register a new student on the database, given the parameters:
        email, name, password, is admin, course, id, profile picture

        Returns a bool indicating the success or failure of the operation.
        '''
        check_email = f'SELECT email FROM Students WHERE email="{email}"'
        self.cursor.execute(check_email)
        exists_email = self.cursor.fetchall()
        if exists_email:
            return False
        profile_pic_data = profile_pic.read()
        if is_admin:
            is_admin = 'TRUE'
        else:
            is_admin = 'FALSE'
        if not id:
            id = 'NULL'
        cmd = f'INSERT INTO Students (email, name, passwd, is_admin, course, id, profile_pic) \
                VALUES ("{email}", "{name}", "{password}", {is_admin}, "{course}", {id}, _binary %s)'
        self.cursor.execute(cmd, (profile_pic_data,))
        self.connection.commit()
        return True

    def manage_admin(self, email: str, is_admin: bool) -> bool:
        '''
        Promote or demote an user, given the parameters: email and is_admin
        (is_admin should be the new status for the user)

        Returns a bool indicating the success or failure of the operation.
        '''
        select_user = f'SELECT email FROM Students WHERE email="{email}"'
        self.cursor.execute(select_user)
        user = self.cursor.fetchall()
        if not user:
            return False
        if is_admin:
            is_admin = 'TRUE'
        else:
            is_admin = 'FALSE'
        query = f'UPDATE Students SET is_admin={is_admin} WHERE email="{email}"'
        try:
            self.cursor.execute(query)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def login(self, email: str, password: str) -> tuple[bool, bool]:
        '''
        Checks if the login data for a student is according to the data stored in the database,
        given the parameters: student email, student password.

        Returns (False, False) if the operation fails, else returns (success, is_admin).
        '''
        select_user = f'SELECT email, passwd, is_admin FROM Students WHERE email="{email}"'
        self.cursor.execute(select_user)
        user = self.cursor.fetchall()
        if not user:
            return False, False
        user = user[0]
        db_password = user[1]
        if password != db_password:
            return False, False
        is_admin = bool(user[2])
        return True, is_admin

    def edit_personal_info(self, email: str, new_email: str = None, name: str = None,
            passwd: str = None, course: str = None, id: int = None, profile_pic = None) -> bool:
        '''
        Edits the personal information for a student, given the parameters
        old email (necessary), new email (optional),
        new name (optional), new password (optional),
        new course (optional), new id (optional)
        new profile picture (optional).

        Returns a bool indicating the success or failure of the operation.
        '''
        queries = []
        if name:
            name_query = f'UPDATE Students SET name="{name}" WHERE email="{email}"'
            queries.append(name_query)
        if passwd:
            passwd_query = f'UPDATE Students SET passwd="{passwd}" WHERE email="{email}"'
            queries.append(passwd_query)
        if course and course != 'NULL':
            course_query = f'UPDATE Students SET course="{course}" WHERE email="{email}"'
            queries.append(course_query)
        if id:
            id_query = f'UPDATE Students SET id={id} WHERE email="{email}"'
            queries.append(id_query)
        if new_email:
            email_query = f'UPDATE Students SET email="{new_email}" WHERE email="{email}"'
            queries.append(email_query)
        if profile_pic:
            pfp_query = f'UPDATE Students SET profile_pic=_binary %s WHERE email="{email}"'
            profile_pic_data = profile_pic.read()
            try:
                self.cursor.execute(pfp_query, (profile_pic_data,))
            except mysql.connector.errors.IntegrityError as e:
                return False
        for query in queries:
            try:
                self.cursor.execute(query)
            except mysql.connector.errors.IntegrityError as e:
                return False
        self.connection.commit()
        return True

    def review_professor(self, student_email: str, prof_id: int, review: str, evaluation: int) -> bool:
        '''
        Review a professor given the parameters: student email, professor id, review, evaluation.

        Returns a bool indicating the success or failure of the operation.
        '''
        cmd = f'INSERT INTO ProfessorReviews VALUES ("{student_email}", {prof_id}, "{review}", {evaluation})'
        try:
            self.cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def review_class(self, student_email: str, class_id: int, review: str, evaluation: int) -> bool:
        '''
        Review a class given the parameters: student email, class id, review, evaluation.

        Returns a bool indicating the success or failure of the operation.
        '''
        cmd = f'INSERT INTO ClassReviews VALUES ("{student_email}", {class_id}, "{review}", {evaluation})'
        try:
            self.cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def del_professor_review(self, student_email: str, professor_name: str = None, professor_id: int = None) -> bool:
        '''
        Deletes a review made for a professor, given the parameters student email AND (professor name OR professor id).

        Returns a bool indicating the success or failure of the operation.
        '''
        if not professor_name and not professor_id:
            return False
        if not professor_id:
            get_professor_id = f'SELECT P.id \
                FROM Professors AS P \
                WHERE P.name="{professor_name}"'
            self.cursor.execute(get_professor_id)
            professor_id = self.cursor.fetchall()[0][0]
        delete_professor_review = f'DELETE \
            FROM ProfessorReviews AS PR \
            WHERE PR.prof_id={professor_id} AND PR.student_email="{student_email}"'
        try:
            self.cursor.execute(delete_professor_review)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def del_class_review(self, student_email: str, class_id: int) -> bool:
        '''
        Deletes a review made for a class, given the parameters student email, class id.

        Returns a bool indicating the success or failure of the operation.
        '''
        delete_class_review = f'DELETE \
            FROM ClassReviews AS CR \
            WHERE CR.student_email="{student_email}" AND CR.class_id={class_id}'
        try:
            self.cursor.execute(delete_class_review)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def edit_professor_review(self, student_email: str, review: str, evaluation: int, prof_name: str = None, prof_id: int = None) -> bool:
        if not prof_name and not prof_id:
            return False
        if not prof_id:
            get_prof_id = f'SELECT P.id \
                FROM Professors AS P \
                WHERE P.name="{prof_name}"'
            self.cursor.execute(get_prof_id)
            prof_id = self.cursor.fetchall()[0][0]
        update_review = f'UPDATE ProfessorReviews \
            SET review="{review}", evaluation={evaluation} \
            WHERE student_email="{student_email}" AND prof_id={prof_id}'
        try:
            self.cursor.execute(update_review)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def edit_class_review(self, student_email: str, class_id: int, review: str, evaluation: int) -> bool:
        update_review = f'UPDATE ClassReviews \
            SET review="{review}", evaluation={evaluation} \
            WHERE student_email="{student_email}" AND class_id={class_id}'
        try:
            self.cursor.execute(update_review)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def report_professor_review(self, student_email: str, prof_id: int) -> bool:
        '''
        Reports a review made for a professor, given the parameters student email and professor id.

        Returns a bool indicating the success or failure of the operation.
        '''
        report_query = f'INSERT INTO ProfessorReviewsReports VALUES ("{student_email}", {prof_id})'
        try:
            self.cursor.execute(report_query)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def report_class_review(self, student_email: str, class_id: int) -> bool:
        '''
        Reports a review made for a class, given the parameters student email and class id.

        Returns a bool indicating the success or failure of the operation.
        '''
        report_query = f'INSERT INTO ClassReviewsReports VALUES ("{student_email}", {class_id})'
        try:
            self.cursor.execute(report_query)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def del_professorreview_report(self, student_email: str, prof_id: int) -> bool:
        '''
        Deletes a report made for a professor review, given the parameters student email and professor id.

        Returns a bool indicating the success or failure of the operation.
        '''
        query = f'DELETE \
            FROM ProfessorReviewsReports as PRR \
            WHERE PRR.student_email="{student_email}" AND PRR.prof_id={prof_id}'
        try:
            self.cursor.execute(query)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def del_classreview_report(self, student_email: str, class_id: int) -> bool:
        '''
        Deletes a report made for a class review, given the parameters student email and class id.

        Returns a bool indicating the success or failure of the operation.
        '''
        query = f'DELETE \
            FROM ClassReviewsReports as CRR \
            WHERE CRR.student_email="{student_email}" AND CRR.class_id={class_id}'
        try:
            self.cursor.execute(query)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    def remove_user(self, email: str) -> bool:
        '''
        Removes an user (student or admin) from the database, given their email.

        Returns a bool indicating the success or failure of the operation.
        '''
        query = f'DELETE \
            FROM Students AS S \
            WHERE S.email="{email}"'
        try:
            self.cursor.execute(query)
        except mysql.connector.errors.IntegrityError as e:
            return False
        self.connection.commit()
        return True

    ###########################################################
    #                      Read functions                     #
    ###########################################################

    def search_discipline(self, name: str) -> list:
        '''
        Gets disciplines with matching name with the search query.

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
        (department name, department id, class id, class term, class code, professor name, professor id)
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

        Returns a list of tuples, each tuple consisting of: (student email, review text, class id)
        '''
        query = f'SELECT student_email, review, evaluation, class_id FROM ClassReviews WHERE class_id={id}'
        self.cursor.execute(query)
        query_result = [i for i in self.cursor.fetchall() if i]
        return query_result

    def get_professorreviews(self, id: int) -> list:
        '''
        Gets all reviews for a professor with a given id.

        Returns a list of tuples, each tuple consisting of: (student email, review text, professor id)
        '''
        query = f'SELECT student_email, review, evaluation, prof_id FROM ProfessorReviews WHERE prof_id={id}'
        self.cursor.execute(query)
        query_result = [i for i in self.cursor.fetchall() if i]
        return query_result

    def get_professorreviews_reports(self) -> list:
        '''
        Gets all professor reviews that were reported by students (users).

        Returns a list of tuples, each tuple consisting of: (student email, review text, professor id)
        '''
        query = f'CALL ProfessorReviewReportsProcedure()' # The actual query for calling procedures in MySQL
        self.cursor.callproc(query[5:-2]) # The MySQL connector for Python has its own way to call procedures
        result = [i.fetchall() for i in self.cursor.stored_results()][0]
        query_result = [i for i in result if i]
        return query_result

    def get_classreviews_reports(self) -> list:
        '''
        Gets all class reviews that were reported by students (users).

        Returns a list of tuples, each tuple consisting of: (student email, review text, class id)
        '''
        query = f'CALL ClassReviewReportsProcedure()' # The actual query for calling procedures in MySQL
        self.cursor.callproc(query[5:-2]) # The MySQL connector for Python has its own way to call procedures
        result = [i.fetchall() for i in self.cursor.stored_results()][0]
        query_result = [i for i in result if i]
        return query_result

    def student_professor_reviews(self, email: str) -> list:
        '''
        Gets all professor reviews that a specific student made, given his email.

        Returns a list of tuples, each tuple consisting of: (professor name, review text)
        '''
        query = f'SELECT P.name, PR.review, PR.evaluation \
            FROM Professors AS P, ProfessorReviews AS PR \
            WHERE P.id=PR.prof_id AND PR.student_email="{email}"'
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        return query_result

    def student_class_reviews(self, email: str) -> list:
        '''
        Gets all class reviews that a specific student made, given his email.

        Returns a list of tuples, each tuple consisting of:
        (class code, discipline name, term, professor name, class schedule, review text, evaluation, class id)
        '''
        query = f'SELECT C.code, D.name, C.term, P.name, C.schedule, CR.review, CR.evaluation, C.id\
            FROM Classes AS C, Disciplines as D, Professors as P, ClassReviews as CR\
            WHERE C.disc_id=D.id AND C.prof_id=P.id AND CR.class_id=C.id AND CR.student_email="{email}"'
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        return query_result

    def student_data(self, email: str) -> tuple:
        '''
        Gets stored data for a student.

        Returns a tuple consisting of: (student name, course, id, profile picture)
        '''
        query = f'SELECT name, course, id, profile_pic FROM Students WHERE email="{email}"'
        self.cursor.execute(query)
        user = self.cursor.fetchall()[0]
        name, course, id, profile_pic = user
        return name, course, id, profile_pic
