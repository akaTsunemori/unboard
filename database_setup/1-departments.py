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
    departments_df = pd.read_csv(PATH + f'departamentos_{term}.csv')
    for idx, data in departments_df.iterrows():
        id = data['cod']
        name = data['nome']
        cmd = f'INSERT INTO Departments VALUES ({id}, "{name}")'
        try:
            cursor.execute(cmd)
        except mysql.connector.errors.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                continue
            print(e)

connection.commit()
