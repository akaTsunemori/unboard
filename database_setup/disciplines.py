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
df = pd.read_csv(PATH + 'disciplinas_2023-1.csv')
df = df.drop_duplicates()

for idx, data in df.iterrows():
    id = data['cod']
    name = data['nome']
    dept_id = data['cod_depto']
    cmd = f'INSERT INTO Disciplines VALUES ("{id}", "{name}", {dept_id})'
    cursor.execute(cmd)

connection.commit()

