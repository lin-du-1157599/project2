-- Drop existing tables to ensure no conflicts.
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS journeys;
DROP TABLE IF EXISTS announcements;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password_hash CHAR(60) BINARY NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    location VARCHAR(50),
    profile_image VARCHAR(255),
    personal_description TEXT,
    role ENUM('traveller', 'editor', 'admin') NOT NULL DEFAULT 'traveller',
    shareable TINYINT NOT NULL DEFAULT 1, -- Indicates whether the user's journeys are shareable (1 = Yes, 0 = No)
    status ENUM('active', 'banned') NOT NULL DEFAULT 'active'
);

CREATE TABLE journeys (
    journey_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('private', 'public') NOT NULL DEFAULT 'private',
    is_hidden TINYINT NOT NULL DEFAULT 0,  -- Indicates whether the journey is hidden (0 = No, 1 = Yes)
    start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- The timestamp when the item was last updated, automatically updated to current time on each update
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT  -- Ensures user_id references a valid user in the users table, preventing deletion of users with associated records
);

CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    journey_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    location VARCHAR(100),
    event_image VARCHAR(255),
    FOREIGN KEY (journey_id) REFERENCES journeys(journey_id) ON DELETE CASCADE  -- Ensures journey_id references a valid journey in the journeys table, and deletes related records if the referenced journey is deleted
);

CREATE TABLE announcements (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') NOT NULL,
    level ENUM('high', 'medium', 'low') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT  -- Ensures user_id references a valid user in the users table, preventing deletion of users with associated records
);

