-- Create the database named "ebookstore" if it doesn't already exist.
CREATE DATABASE IF NOT EXISTS ebookstore;

-- Select the "ebookstore" database for use.  This makes it the active database.
USE ebookstore;

-- Create the "book" table within the "ebookstore" database.
CREATE TABLE book (
    id INT,           -- Unique identifier for the book (e.g., 3001, 3002).  Consider making this the primary key.
    title VARCHAR(100), -- Title of the book (e.g., "A Tale of Two Cities").  Increased to 100.
    author VARCHAR(50),  -- Author of the book (e.g., "Charles Dickens"). Increased to 50.
    qty INT          -- Quantity of books in stock.
);

-- Insert data into the "book" table.  Each row represents a book.
INSERT INTO book (id, title, author, qty) VALUES
(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
(3002, 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 40),
(3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
(3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
(3005, 'Alice in Wonderland', 'Lewis Carroll', 12);

-- You can use this to see the table you created
SELECT * FROM book;
