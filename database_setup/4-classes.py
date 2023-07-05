import pandas as pd
import mysql.connector


connection = mysql.connector.connect(
    host='localhost',
    user='unboard_admin',
    password='unboard_passwd',
    database='unboard'
)
cursor = connection.cursor()


PATH = '~/Downloads/ofertas_sigaa/data/2023.1/'
df = pd.read_csv(PATH + 'turmas_2023-1.csv')
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
        prof_name = prof_name[:-1]
    prof_name = ' '.join(prof_name)
    if not prof_name:
        continue
    prof_id = professors[prof_name]
    disc_id = data['cod_disciplina']
    schedule = data['periodo']
    cmd = f'INSERT INTO Classes (code, disc_id, term, prof_id, schedule) VALUES ("{code}", "{disc_id}", "{term}", {prof_id}, "{schedule}")'
    try:
        cursor.execute(cmd)
    except mysql.connector.errors.IntegrityError as e:
        print(e)
        continue

connection.commit()
