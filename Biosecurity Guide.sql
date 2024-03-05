DROP SCHEMA IF EXISTS biosecurity;
CREATE SCHEMA biosecurity;
USE biosecurity;

CREATE TABLE IF NOT EXISTS user (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  role ENUM('agronomist', 'staff', 'admin') NOT NULL,
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS agronomist (
  agronomist_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  address VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
  phone_number VARCHAR(20),
  date_joined DATE NOT NULL,
  status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
  PRIMARY KEY (agronomist_id),
  UNIQUE (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS staffadmin (
  staff_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
  work_phone_number VARCHAR(20),
  hire_date DATE,
  position VARCHAR(45),
  department VARCHAR(45),
  status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
  PRIMARY KEY (staff_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS biosecurity_guide (
  agriculture_id INT NOT NULL AUTO_INCREMENT,
  item_type ENUM('pest', 'disease') NOT NULL,
  common_name VARCHAR(100) NOT NULL,
  scientific_name VARCHAR(100),
  key_characteristics TEXT,
  biology_description TEXT,
  impacts TEXT,
  control TEXT,
  primary_image VARCHAR(255),
  PRIMARY KEY (agriculture_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS images (
  image_id INT NOT NULL AUTO_INCREMENT,
  agriculture_id INT NOT NULL,
  image_path VARCHAR(255) NOT NULL,
  caption VARCHAR(255),
  FOREIGN KEY (agriculture_id) REFERENCES biosecurity_guide(agriculture_id) ON DELETE CASCADE,
  PRIMARY KEY (image_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/* Insert 9 users into user table */
INSERT INTO user (username, password, email, role) VALUES 
('ryan', 'ryan1214', 'ryan@gmail.com', 'agronomist'),
('ray', 'ray12345', 'ray@gmail.com', 'agronomist'),
('lukia', 'lukia1234', 'lukia@gmail.com', 'agronomist'),
('luna', 'luna1234', 'luna@gmail.com', 'agronomist'),
('lina', 'lina1234', 'lina@gmail.com', 'agronomist'),
('lana', 'lana1234', 'lana@gmail.com', 'staff'),
('leila', 'leila1234', 'leila@gmail.com', 'staff'),
('lycan', 'lycan1234', 'lycan@gmail.com', 'staff'),
('byan', 'byan1234', 'byan@gmail.com', 'admin');

/* Insert 5 agronomists into the agronomist table */
INSERT INTO agronomist (user_id, first_name, last_name, address, email, phone_number, date_joined, status)
SELECT 
    user_id, 
    CASE email 
        WHEN 'ryan@gmail.com' THEN 'Ryan'
        WHEN 'ray@gmail.com' THEN 'Ray'
        WHEN 'lukia@gmail.com' THEN 'Lukia'
        WHEN 'luna@gmail.com' THEN 'Luna'
        WHEN 'lina@gmail.com' THEN 'Lina'
    END, 
    CASE email 
        WHEN 'ryan@gmail.com' THEN 'Tay'
        WHEN 'ray@gmail.com' THEN 'Lee'
        WHEN 'lukia@gmail.com' THEN 'Swift'
        WHEN 'luna@gmail.com' THEN 'Moofung'
        WHEN 'lina@gmail.com' THEN 'Inverse'
    END, 
    '123 Abc Ave', -- Assuming same address for simplification
    email, 
    CASE email 
        WHEN 'ryan@gmail.com' THEN '555-0102'
        WHEN 'ray@gmail.com' THEN '555-0103'
        WHEN 'lukia@gmail.com' THEN '555-0104'
        WHEN 'luna@gmail.com' THEN '555-0105'
        WHEN 'lina@gmail.com' THEN '555-0106'
    END, -- Unique phone numbers
    CURDATE(), -- Assuming the current date for date_joined
    'active'
FROM user 
WHERE role = 'agronomist';

/* Insert 3 staff and 1 admin details into staff_admin table */
INSERT INTO staffadmin (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status)
SELECT user_id, 'Lana', 'Doe', email, '888-0101', '2020-02-09', 'Staff', 'Management', 'active'
FROM user WHERE email = 'lana@gmail.com'
UNION
SELECT user_id, 'Leila', 'Smith', email, '888-0102', '2021-01-01', 'Staff', 'Operation', 'active'
FROM user WHERE email = 'leila@gmail.com'
UNION
SELECT user_id, 'Lycan', 'Wolf', email, '888-0103', '2022-02-02', 'Staff', 'Operation', 'active'
FROM user WHERE email = 'lycan@gmail.com'
UNION
SELECT user_id, 'Byan', 'King', email, '888-0104', '2023-03-03', 'Admin', 'Management', 'active'
FROM user WHERE email = 'byan@gmail.com';



