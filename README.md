
<h1 align="center">
  <br>
  <a href="https://github.com/akaTsunemori/unboard"><img src="https://i.imgur.com/uHPOF99.png" alt="anime-image" width="200"></a>
  <br>
  UnBoard
  <br>
</h1>

<h4 align="center">Um website dedicado a todos os alunos da <a href="https://unb.br/" target="_blank">UnB</a>, com intuito de permitir que alunos avaliem professores e turmas.</h4>

<p align="center">
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#como-usar">Como usar</a> •
  <a href="#créditos">Créditos</a> •
  <a href="#licença">Licença</a>
</p>

![screenshot](https://i.imgur.com/smyt7md.png)

## Funcionalidades

* Avaliação de professores
  - Cadastre-se e avalie todos os professores da UnB!
* Avaliação de turmas
  - Professor bom, mas foi péssimo em alguma matéria específica? Avalie exclusivamente a turma que ele ministrou, no semestre que isso aconteceu.
* Moderação
  - Através da conta de administrador, as avaliações são moderadas e qualquer comentário ofensivo não é tolerado.
* Banco de dados extenso
  - Dados de todas as turmas e professores dos últimos 3 semestres da UnB.
* Painel do estudante
  - Acesse todas as avaliações que você já fez em um único lugar.
* Interface amigável
  - Interface cuidadosamente planejada para a melhor experiência de usuário.

## Roadmap

Lista com o progresso do website:

- [x] Separação das páginas do aplicativo
- [x] Layout bruto da interface
- [x] Estilização básica da interface
- [x] Definir stubs para o banco de dados ainda não implementado
- [x] Funcionalidades simples do Front-End
- [x] Implementação do banco de dados
- [x] Estilização avançada
- [x] Polimento e detalhes finais

## Instalação

Para clonar e executar o website, será necessário que as tecnologias [Git](https://git-scm.com), [MySQL](https://www.mysql.com/), [Python](https://www.python.org/) e [pip](https://pip.pypa.io/en/stable/index.html) estejam instaladas em seu computador, além de um browser capaz de JavaScript. Os seguintes comandos devem ser executados em um Terminal:

```bash
# Clonar este repositório
$ git clone https://github.com/akaTsunemori/unboard.git

# Mudar o diretório corrente ao do repositório
$ cd unboard

# Instalar dependências
$ pip install -r requirements.txt

# Fazendo login no MySQL como usuário root
mysql -u root -p

# Criação de usuário MySQL
CREATE USER 'unboard_admin'@'localhost' IDENTIFIED BY 'unboard_passwd';

# Criação da database unboard;
CREATE DATABASE unboard;

# Sair do ambiente MySQL
exit;

# Organizar o banco de dados e suas tabelas
mysql -u root -p unboard < ./database_setup/unboard.sql

# Sair do ambiente MySQL
exit;

# Alimentar o banco de dados
python3 ./database_setup/1-departments.py
python3 ./database_setup/2-disciplines.py
python3 ./database_setup/3-professors.py
python3 ./database_setup/4-classes.py

# Executar a aplicação
$ python3 app.py
```

> **Notas:**<br>
> - As instruções acima foram direcionadas a um ambiente Linux.<br>
> - Assume-se que o setup do MySQL tenha sido feito corretamente, e que nele haja um usuário root para fazer as operações básicas de criação de usuário, tabelas etc.
> - As instruções sobre o MySQL assumem que não existe, previamente, uma database chamada *unboard*, nem um usuário chamado *unboard_admin*.<br>
> - O primeiro usuário Administrador do sistema será inserido automaticamente pelo script *unboard.sql*, a presença desse primeiro usuário é necessária.

## Como usar

Para acessar o website, basta abrir um browser qualquer (Firefox ou Chrome, por exemplo) e se direcionar ao site *localhost:5000*. Uma vez que todo o setup tenha sido executado com sucesso, referencie-se ao vídeo presente no relatório, que apresenta a usabililidade do aplicativo.

## Créditos

Esse software usa os seguintes módulos de código aberto:

- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- [pandas](https://pandas.pydata.org/)
- [unidecode](https://pypi.org/project/Unidecode/)

## Licença

GNU GENERAL PUBLIC LICENSE<br>
Version 2, June 1991

---

> GitHub [@akaTsunemori](https://github.com/akaTsunemori)

