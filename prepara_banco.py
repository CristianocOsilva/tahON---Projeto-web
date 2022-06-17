import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='#Computacao2354'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `fornecedor`;")

cursor.execute("CREATE DATABASE `fornecedor`;")

cursor.execute("USE `fornecedor`;")

# criando tabelas
TABLES = {}
TABLES['Fornecedores'] = ('''
      CREATE TABLE `fornecedores` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `cnpj` varchar(30) NOT NULL,
      `ramo` varchar(30) NOT NULL,
      `endereco` varchar(50) NOT NULL,
      `telefone` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `id` int(11) NOT NULL AUTO_INCREMENT,    
      `nome` varchar(50) NOT NULL,
      `email` varchar(50) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Cristiano Silva", "cristianosilva@gmail.com", generate_password_hash("cristiano").decode('utf-8')),
      ("Karina Nielsen", "karina@uol.com.br", generate_password_hash("karina").decode('utf-8')),
      ("Guilherme Silva", "guilherme@teste.com", generate_password_hash("guilherme").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
fornecedores_sql = 'INSERT INTO fornecedores (nome, cnpj, ramo, endereco, telefone) VALUES (%s, %s, %s, %s, %s)'
fornecedores = [
      ('Casas Bahia', '11.555.444/0001-02', 'Varejo', 'Av Pacaembu s/n', '11-40030002'),
      ('Atacadao', '22.433.255/0001-01', 'Atacado', 'Rua Itapemirim 25, Osasco, SP', '11-20020304'),
      ('Boticario', '33.749.285/0001-04', 'Varejo', 'Av Pacaembu s/n', '11-40030002'),
      ('Cacau Show', '44.546.758/0001-06', 'Varejo', 'Av Pacaembu s/n', '11-40030002'),
      ('Ambev', '55.432.351/0001-09', 'Bebidas', 'Av Pacaembu s/n', '11-40030002'),
      ('Petrobras', '00.256.349/0001-23', 'Combustivel', 'Av Pacaembu s/n', '11-40030002'),
]
cursor.executemany(fornecedores_sql, fornecedores)

cursor.execute('select * from fornecedores')
print(' -------------  Fornecedores:  -------------')
for fornecedor in cursor.fetchall():
    print(fornecedor[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()