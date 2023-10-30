-- Create Database
DROP DATABASE IF EXISTS blogly;
CREATE DATABASE blogly;
\c blogly_db;

CREATE TABLE users (
    id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    image_url VARCHAR(300)
);