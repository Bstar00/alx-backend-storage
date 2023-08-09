-- Create the 'users' table if it doesn't exist
-- ADD country, enumeration of countries: US, CO and TN, never null
-- US  as defualt country
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
