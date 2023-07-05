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
departments_df = pd.read_csv(PATH + 'departamentos_2023-1.csv')

for idx, data in departments_df.iterrows():
    id = data['cod']
    name = data['nome']
    cmd = f'INSERT INTO Departments VALUES ({id}, "{name}")'
    cursor.execute(cmd)

connection.commit()
