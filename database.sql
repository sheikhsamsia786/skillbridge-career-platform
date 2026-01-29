CREATE DATABASE IF NOT EXISTS skillbridge;
USE skillbridge;

CREATE TABLE IF NOT EXISTS custom_roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255),
    description TEXT,
    steps TEXT
);

select * from  custom_roadmaps;

ALTER TABLE custom_roadmaps
ADD COLUMN progress INT DEFAULT 0;

DELETE FROM custom_roadmaps;

ALTER TABLE custom_roadmaps
ADD COLUMN steps_json LONGTEXT;

