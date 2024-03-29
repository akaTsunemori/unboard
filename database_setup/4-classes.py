import pandas as pd
import mysql.connector


connection = mysql.connector.connect(
    host='localhost',
    user='unboard_admin',
    password='unboard_passwd',
    database='unboard'
)
cursor = connection.cursor()

terms = ['2023-1', '2022-2', '2022-1']
PATH = './database_setup/data/'
for t in terms:
    df = pd.read_csv(PATH + f'turmas_{t}.csv')
    df = df.drop_duplicates()

    professors = dict()
    professors_query = 'SELECT id, name FROM Professors';
    cursor.execute(professors_query)
    professors_db = cursor.fetchall()
    for id, name in professors_db:
        professors[name] = id

    for idx, data in df.iterrows():
        code = data['turma']
        term = data['periodo']
        p = data['professor']
        prof_name = p.split()
        if prof_name[-1][-1] == ')':
            prof_name.pop()
        prof_name = ' '.join(prof_name)
        if not prof_name:
            continue
        prof_id = professors[prof_name]
        disc_id = data['cod_disciplina']
        schedule = data['horario']
        cmd = f'INSERT INTO Classes (code, disc_id, term, prof_id, schedule) VALUES ("{code}", "{disc_id}", "{term}", {prof_id}, "{schedule}")'
        try:
            cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                continue
            print(e)

connection.commit()
