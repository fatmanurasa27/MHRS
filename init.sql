CREATE DATABASE IF NOT EXISTS mhrs;
USE mhrs;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS appointment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    date VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

-- Doktorları ve Bölümleri Ekleyelim
INSERT INTO doctor (name, department) VALUES 
('Dr. Ali Yılmaz', 'Kardiyoloji'),
('Dr. Ayşe Demir', 'Kardiyoloji'),
('Dr. Mehmet Kaya', 'Nöroloji'),
('Dr. Fatma Çelik', 'Nöroloji'),
('Dr. Mustafa Can', 'Ortopedi'),
('Dr. Zeynep Şahin', 'Ortopedi'),
('Dr. Burak Yıldız', 'Dahiliye'),
('Dr. Elif Aydın', 'Dahiliye'),
('Dr. Caner Tekin', 'Göz Hastalıkları'),
('Dr. Seda Korkmaz', 'Göz Hastalıkları'),
('Dr. Emre Polat', 'Cildiye'),
('Dr. Aslı Erdoğan', 'Cildiye');