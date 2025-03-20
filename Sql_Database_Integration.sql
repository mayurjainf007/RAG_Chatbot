-- Create PostgreSQL Database for Policy Storage
CREATE DATABASE healthcare_policies;

-- Switch to the new database
\c healthcare_policies;

-- Create a table to store policy data
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO policies (title, content) VALUES
('Policy A', 'Covers general health expenses including hospitalization.'),
('Policy B', 'Includes maternity benefits and childcare.'),
('Policy C', 'Covers dental and vision care expenses.');

-- Query to fetch all policies
SELECT * FROM policies;
