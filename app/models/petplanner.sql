DROP DATABASE IF EXISTS PetPlanner;
CREATE DATABASE PetPlanner;
USE PetPlanner;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY
    , email VARCHAR(255) UNIQUE NOT NULL
    , password VARCHAR(255) NOT NULL
    , name VARCHAR(100)
    , role VARCHAR(50) NOT NULL
    , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pets (
    id INT AUTO_INCREMENT PRIMARY KEY
    , user_id INT NOT NULL
    , name VARCHAR(100) NOT NULL
    , breed VARCHAR(100)
    , birth_date DATE
    , physical_characteristics TEXT
    , health_conditions TEXT
    , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE allergies (
    id INT AUTO_INCREMENT PRIMARY KEY
    , name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE pet_allergies (
    pet_id INT
    , allergy_id INT
    , PRIMARY KEY (pet_id, allergy_id)
    , FOREIGN KEY (pet_id) REFERENCES pets(id)
    , FOREIGN KEY (allergy_id) REFERENCES allergies(id)
);

CREATE TABLE medical_events (
    id INT AUTO_INCREMENT PRIMARY KEY
    , pet_id INT
    , title VARCHAR(255) NOT NULL
    ,description TEXT
    , date DATE NOT NULL
    , is_completed BOOLEAN
    , recurrence VARCHAR(50)
    , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , FOREIGN KEY (pet_id) REFERENCES pets(id)
);

CREATE TABLE centers (
    id INT AUTO_INCREMENT PRIMARY KEY
    , user_id INT
    , name VARCHAR(255) NOT NULL
    , address TEXT
    , hours VARCHAR(255)
    , services TEXT
    , type VARCHAR(50) NOT NULL
    , FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY
    , author_id INT
    , title VARCHAR(255) NOT NULL
    , content TEXT NOT NULL
    , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , updated_at TIMESTAMP NULL
    , FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY
    , event_id INT
    , scheduled_at TIMESTAMP NULL
    , sent BOOLEAN
    , FOREIGN KEY (event_id) REFERENCES medical_events(id)
);