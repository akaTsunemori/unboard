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
df = df['professor']
professors = set()
for i in df:
    prof = i.split()
    if i[-1][-1] == ')':
        prof = prof[:-1]
    professors.add(' '.join(prof))


if '' in professors:
    professors.remove('')


result = list(professors)
for name in result:
    cmd = f'INSERT INTO Professors (name) VALUES ("{name}")'
    cursor.execute(cmd)

connection.commit()

