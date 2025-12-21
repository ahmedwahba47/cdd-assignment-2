-- Initialize database for Book Service
-- This script runs automatically when MySQL container starts for the first time

USE bookdb;

-- Create books table if not exists (JPA will also create this, but this ensures proper setup)
CREATE TABLE IF NOT EXISTS books (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    description VARCHAR(1000),
    published_year INT,
    quantity INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_author (author),
    INDEX idx_isbn (isbn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Grant privileges
GRANT ALL PRIVILEGES ON bookdb.* TO 'bookuser'@'%';
FLUSH PRIVILEGES;
