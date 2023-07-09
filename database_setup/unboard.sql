USE unboard;
GRANT ALL PRIVILEGES ON unboard TO 'unboard_admin'@'localhost';
GRANT ALL PRIVILEGES ON unboard.* TO 'unboard_admin'@'localhost';

CREATE TABLE Emails (
  email VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE Students (
  email VARCHAR(50) PRIMARY KEY NOT NULL,
  name VARCHAR(200) NOT NULL,
  passwd VARCHAR(32) NOT NULL,
  profile_pic MEDIUMBLOB,
  FOREIGN KEY (email) REFERENCES Emails(email) ON DELETE CASCADE
);

CREATE TABLE Admins (
  email VARCHAR(50) PRIMARY KEY NOT NULL,
  passwd VARCHAR(32) NOT NULL,
  FOREIGN KEY (email) REFERENCES Emails(email) ON DELETE CASCADE
);

CREATE TABLE Professors (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  name VARCHAR(200) NOT NULL,
  CONSTRAINT uc_Professors UNIQUE (name)
);

CREATE TABLE Departments (
  id INT PRIMARY KEY NOT NULL,
  name VARCHAR(200) NOT NULL
);

CREATE TABLE Disciplines (
  id VARCHAR(20) NOT NULL,
  name VARCHAR(400) NOT NULL,
  dept_id INT NOT NULL,
  PRIMARY KEY (id, name),
  FOREIGN KEY (dept_id) REFERENCES Departments(id) ON DELETE CASCADE
);

CREATE TABLE Classes (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  code VARCHAR(20) NOT NULL,
  disc_id VARCHAR(20) NOT NULL,
  term VARCHAR(20) NOT NULL,
  prof_id INT NOT NULL,
  schedule VARCHAR(500) NOT NULL,
  CONSTRAINT uc_Classes UNIQUE (code, disc_id, term, prof_id, schedule),
  FOREIGN KEY (disc_id) REFERENCES Disciplines(id) ON DELETE CASCADE,
  FOREIGN KEY (prof_id) REFERENCES Professors(id) ON DELETE CASCADE
);

CREATE TABLE ClassReviews (
  student_email VARCHAR(50) NOT NULL,
  class_id INT NOT NULL,
  review TEXT NOT NULL,
  evaluation INT NOT NULL CHECK (evaluation BETWEEN 1 AND 5),
  PRIMARY KEY (student_email, class_id),
  FOREIGN KEY (student_email) REFERENCES Students(email) ON DELETE CASCADE,
  FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE CASCADE
);

CREATE TABLE ProfessorReviews (
  student_email VARCHAR(50) NOT NULL,
  prof_id INT NOT NULL,
  review TEXT NOT NULL,
  evaluation INT NOT NULL CHECK (evaluation BETWEEN 1 AND 5),
  PRIMARY KEY (student_email, prof_id),
  FOREIGN KEY (student_email) REFERENCES Students(email) ON DELETE CASCADE,
  FOREIGN KEY (prof_id) REFERENCES Professors(id) ON DELETE CASCADE
);

CREATE TABLE ClassReviewsReports (
  student_email VARCHAR(50) NOT NULL,
  class_id INT NOT NULL,
  PRIMARY KEY (student_email, class_id),
  FOREIGN KEY (student_email) REFERENCES Students(email) ON DELETE CASCADE,
  FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE CASCADE
);

CREATE TABLE ProfessorReviewsReports (
  student_email VARCHAR(50) NOT NULL,
  prof_id INT NOT NULL,
  PRIMARY KEY (student_email, prof_id),
  FOREIGN KEY (student_email) REFERENCES Students(email) ON DELETE CASCADE,
  FOREIGN KEY (prof_id) REFERENCES Professors(id) ON DELETE CASCADE
);

CREATE VIEW ProfessorReviewReportsView AS
SELECT PRR.student_email, PR.review, PR.evaluation, PRR.prof_id
FROM ProfessorReviews AS PR JOIN ProfessorReviewsReports AS PRR
ON PR.student_email = PRR.student_email AND PR.prof_id = PRR.prof_id;

CREATE VIEW ClassReviewReportsView AS
SELECT CRR.student_email, CR.review, CR.evaluation, CRR.class_id
FROM ClassReviews AS CR JOIN ClassReviewsReports AS CRR
ON CR.student_email=CRR.student_email AND CR.class_id=CRR.class_id;

DELIMITER //
CREATE PROCEDURE ProfessorReviewReportsProcedure() BEGIN
SELECT * FROM ProfessorReviewReportsView; END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ClassReviewReportsProcedure() BEGIN
SELECT * FROM ClassReviewReportsView; END //
DELIMITER ;

INSERT INTO Emails VALUES ("admin@unb.br");
INSERT INTO Admins VALUES ("admin@unb.br", "admin");
