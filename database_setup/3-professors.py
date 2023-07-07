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
for term in terms:
    df = pd.read_csv(PATH + f'turmas_{term}.csv')
    df = df['professor']
    professors = set()
    for i in df:
        prof = i.split()
        if i[-1][-1] == ')':
            prof.pop()
        professors.add(' '.join(prof))

    if '' in professors:
        professors.remove('')

    result = list(professors)
    for name in result:
        cmd = f'INSERT INTO Professors (name) VALUES ("{name}")'
        try:
            cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                continue
            print(e)

connection.commit()
