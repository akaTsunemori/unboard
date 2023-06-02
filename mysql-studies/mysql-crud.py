import mysql.connector


# Nao esquecer de dar start no service mysqld
# Importar DB: sudo mysql -u username -p database_name < sql_file_path
# Exportar DB: sudo mysqldump -u username -p database_to_export > file.sql


# Abrir conexao e cursor
connection = mysql.connector.connect(
    host='localhost',
    user='lordq',
    password='9468',
    database='test'
)
cursor = connection.cursor()

# CREATE
cmd = 'INSERT INTO Person (Id, name, last_name) VALUES (420, "Chuu", "do Loona")'
cursor.execute(cmd)
connection.commit()

# READ
cmd = 'SELECT * FROM Person WHERE Id = "420"'
cursor.execute(cmd)
resultado = cursor.fetchall()
print(resultado)

# UPDATE
cmd = 'UPDATE Person SET Id = 69 WHERE name="Chuu"'
cursor.execute(cmd)
connection.commit()

# DELETE
cmd = 'DELETE FROM Person WHERE Id = 69'
cursor.execute(cmd)
connection.commit()

# Fechar cursor e conexao
cursor.close()
connection.close()
