CREATE TABLE courses (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(350),
    pet ENUM('Dogs', 'Cats', 'Hamster', 'Ferrets', 'Parrots'),
    level ENUM('Beginner', 'Intermediate', 'Advanced'),
    start_date DATE,
    start_time DATETIME,
    duration ENUM('45','60','90'),
    length ENUM('4','6','8'),
    trainer_name VARCHAR(350),
    description TEXT
)ENGINE=INNODB;

insert into courses (name, pet, level, start_date, start_time, duration, length, trainer_name, description) values 
("Morning Obedience","Dogs","Beginner","2022-9-07","08:00:00", "45", "4","Pie Caso","Get the best pics of your pet")
;

CREATE TABLE attendees (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(350),
    last_name VARCHAR(350),
    phone_number VARCHAR(350),
    email VARCHAR(350),
    birth_date DATE,
    course_id int,
    FOREIGN KEY (course_id) REFERENCES courses(id)
)ENGINE=INNODB;