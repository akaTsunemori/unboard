INSERT INTO Students (email, name, passwd, is_admin)
VALUES ("arthur@unb.br", "Arthur Carvalho", "1234", FALSE);
INSERT INTO Students (email, name, passwd, is_admin)
VALUES ("dani@unb.br", "Danielle Stephane", "1234", FALSE);
INSERT INTO Students (email, name, passwd, is_admin)
VALUES ("yaya@unb.br", "Yasmim Wenzel", "1234", FALSE);

INSERT INTO Professors (name)
VALUES ("PEDRO GARCIA FREITAS");
INSERT INTO Professors (name)
VALUES ("EDUARDO PEIXOTO FERNANDES DA SILVA");
INSERT INTO Professors (name)
VALUES ("LELIO RIBEIRO SOARES JUNIOR");

INSERT INTO Departments (id, name)
VALUES (443, "DEPTO ENGENHARIA ELETRICA - BRASÍLIA");
INSERT INTO Departments (id, name)
VALUES (508, "DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA");
INSERT INTO Departments (id, name)
VALUES (424, "DEPTO NUTRICAO - BRASÍLIA");

INSERT INTO Disciplines
VALUES ("CIC0097", "BANCOS DE DADOS", 508);
INSERT INTO Disciplines
VALUES ("ENE0068", "SINAIS E SISTEMAS EM TEMPO DISCRETO", 443);
INSERT INTO Disciplines
VALUES ("ENE0067", "SINAIS E SISTEMAS EM TEMPO CONTÍNUO", 443);

INSERT INTO Classes (code, disc_id, term, prof_id, schedule)
VALUES ("01", "CIC0097", "2023.1", 1, "35T45");
INSERT INTO Classes (code, disc_id, term, prof_id, schedule)
VALUES ("02", "ENE0067", "2023.1", 3, "35M34");
INSERT INTO Classes (code, disc_id, term, prof_id, schedule)
VALUES ("02", "ENE0068", "2023.1", 2, "35M34");

INSERT INTO ClassReviews VALUES
("arthur@unb.br", 2, "As aulas enrolaram muito", 3),
("dani@unb.br", 1, "Gostei de cursar a disciplina, embora o trabalho final tenha sido pesado.", 5),
("yaya@unb.br", 3, "Os projetos dessa matéria são muito interessantes!", 5);

INSERT INTO ClassReviewsReports
VALUES ("dani@unb.br", 1), ("arthur@unb.br", 2), ("yaya@unb.br", 3);

INSERT INTO ProfessorReviews VALUES
("arthur@unb.br", 1, "Professor bem legal :)", 5),
("dani@unb.br", 3, "Assisti 1 aula dele e nao entendi nada :D", 5),
("yaya@unb.br", 2, "Curti as aulas dele.", 5);

INSERT INTO ProfessorReviewsReports
VALUES ("arthur@unb.br", 1), ("yaya@unb.br", 2), ("dani@unb.br", 3);