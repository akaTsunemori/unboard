CREATE USER 'unboard_admin'@'localhost' IDENTIFIED BY 'unboard_passwd';

CREATE DATABASE unboard;
USE unboard;
GRANT ALL PRIVILEGES ON unboard TO 'unboard_admin'@'localhost';
GRANT ALL PRIVILEGES ON unboard.* TO 'unboard_admin'@'localhost';

CREATE TABLE Students (
  email VARCHAR(50) PRIMARY KEY NOT NULL,
  name VARCHAR(200) NOT NULL,
  passwd VARCHAR(32) NOT NULL,
  profile_pic MEDIUMBLOB NOT NULL
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
  PRIMARY KEY (student_email, class_id),
  FOREIGN KEY (student_email) REFERENCES Students(email) ON DELETE CASCADE,
  FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE CASCADE
);

CREATE TABLE ProfessorReviews (
  student_email VARCHAR(50) NOT NULL,
  prof_id INT NOT NULL,
  review TEXT NOT NULL,
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