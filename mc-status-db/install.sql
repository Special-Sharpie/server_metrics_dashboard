-- install.sql
-- Generic SQL install file
-- Intended for initializing a new database environment

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS server_metrics
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Use the new database
USE server_metrics;

-- Optional: Set default SQL mode and time zone
SET sql_mode = 'STRICT_ALL_TABLES';
SET time_zone = '+00:00';

-- Create events table
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    event BOOLEAN NOT NULL COMMENT "0 Disconnect, 1 Connect",
    `timestamp` INT NOT NULL COMMENT "Timestamp when the event occurred"
);

-- Create positions table
CREATE TABLE positions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  x INT NOT NULL,
  y INT NOT NULL,
  z INT NOT NULL,
  username VARCHAR(16) NOT NULL,
  `timestamp` INT NOT NULL
);

-- Create logs table
CREATE TABLE logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  `message` VARCHAR(2048) NOT NULL,
  `level` VARCHAR(10) NOT NULL,
  `timestamp` INT NOT NULL
);
