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
    df = pd.read_csv(PATH + f'disciplinas_{term}.csv')
    for idx, data in df.iterrows():
        id = data['cod']
        name = data['nome']
        dept_id = data['cod_depto']
        cmd = f'INSERT INTO Disciplines VALUES ("{id}", "{name}", {dept_id})'
        try:
            cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                continue
            print(e)

connection.commit()
