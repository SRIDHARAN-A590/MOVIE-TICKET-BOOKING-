-- =============================================
-- FIX SCRIPT: Movie Booking System Database
-- Run this in MySQL Workbench to clean & reset data
-- =============================================

USE movie_booking_system;

-- STEP 1: Disable foreign key checks to allow truncation
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE PAYMENT;
TRUNCATE TABLE BOOKING_SEAT;
TRUNCATE TABLE BOOKING;
TRUNCATE TABLE SEAT;
TRUNCATE TABLE SHOWS;
TRUNCATE TABLE THEATRE;
TRUNCATE TABLE MOVIES;
TRUNCATE TABLE USERS;
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- STEP 2: USERS
-- =============================================
INSERT INTO USERS (name, email, password_hash, role) VALUES 
('Admin User',   'admin@gmail.com',               '$2b$12$y6eZemMQyxbW/gjIe0/BTO/4txZXHMBZapsvrlrYz/ytDnS80tEly', 'admin'),
('John Doe',     'john@example.com',              '$2b$12$ieVpH4QnmIr3GpJsVaaLq.944qSO7rLo7j6z.PZXwQgBEZ5J0Xs1G', 'customer'),
('Jane Smith',   'jane@example.com',              '$2b$12$ieVpH4QnmIr3GpJsVaaLq.944qSO7rLo7j6z.PZXwQgBEZ5J0Xs1G', 'customer'),
('Sridharan K',  'sridharanak032006@gmail.com',   '$2b$12$ieVpH4QnmIr3GpJsVaaLq.944qSO7rLo7j6z.PZXwQgBEZ5J0Xs1G', 'customer');

-- =============================================
-- STEP 3: MOVIES (19 titles)
-- =============================================
INSERT INTO MOVIES (title, description, duration_mins, genre, language, release_date, poster_url) VALUES 
('The Batman',              'Corruption in Gotham City.',           176, 'Action',    'English', '2022-03-04', 'https://img10.hotstar.com/image/upload/f_auto,q_auto/sources/r1/cms/prod/4142/1776237014142-i'),
('Dune',                    'War for the desert planet Arrakis.',   155, 'Sci-Fi',    'English', '2021-10-22', 'https://media.newyorker.com/photos/61772f3f7a6eb9892dafd2c1/master/pass/Park-Dune.jpg'),
('Spider-Man: No Way Home', 'Peter faces multiversal threats.',     148, 'Action',    'English', '2021-12-17', 'https://images.indianexpress.com/2021/11/spider-man-no-way-home-1200-2.jpg'),
('Inception',               'Extracting secrets from dreams.',      148, 'Sci-Fi',    'English', '2010-07-16', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_g6LtC3x4Ddfav_XPzw-iQ_f4MqlPMkYYuQ&s'),
('Interstellar',            'NASA journey to find a new home.',     169, 'Sci-Fi',    'English', '2014-11-07', 'https://m.media-amazon.com/images/I/814E2+pjjzL._AC_SL1500_.jpg'),
('Oppenheimer',             'The enigma of the atomic bomb.',       180, 'Biography', 'English', '2023-07-21', 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/Oppenheimer_%28film%29.jpg/250px-Oppenheimer_%28film%29.jpg'),
('Barbie',                  'Stereotypical Barbie crisis.',         114, 'Comedy',    'English', '2023-07-21', 'https://upload.wikimedia.org/wikipedia/en/0/0b/Barbie_2023_poster.jpg'),
('Jailer 2',                'The return of the tiger.',             170, 'Action',    'Tamil',   '2025-08-10', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREvB05WGBe19rb24kCGUjudps-H63oIAGfcw&s'),
('Leo',                     'A calm before the storm.',             164, 'Action',    'Tamil',   '2023-10-19', 'https://images.indianexpress.com/2023/10/leo-review-19102023.jpg'),
('RRR',                     'The epic brotherhood.',                187, 'Action',    'Telugu',  '2022-03-25', 'https://m.media-amazon.com/images/I/81XSirG7qFL._UF894,1000_QL80_.jpg'),
('Animal',                  'Family, blood, and fury.',             201, 'Drama',     'Hindi',   '2023-12-01', 'https://m.media-amazon.com/images/M/MV5BZThmNDg1NjUtNWJhMC00YjA3LWJiMjItNmM4ZDQ5ZGZiN2Y2XkEyXkFqcGc@._V1_.jpg'),
('Pushpa: The Rise',        'Sandalwood smuggler.',                 179, 'Action',    'Telugu',  '2021-12-17', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43EpXkB8hyRy47_DBdbZI3kmLMxn7dJdjOA&s'),
('Vikram',                  'The high-octane thriller.',            175, 'Action',    'Tamil',   '2022-06-03', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG_4DuNSmYs7fdFTTDdE1TZYwoMYk-RLuNjw&s'),
('Kantara',                 'Divine justice.',                      148, 'Thriller',  'Kannada', '2022-09-30', 'https://i0.wp.com/ficklesorts.com/wp-content/uploads/2024/04/kantara-featured.jpg'),
('Varanasi',                'Mahesh Babu in Rajamouli epic.',       175, 'Adventure', 'Hindi',   '2026-07-21', 'https://static.wixstatic.com/media/7c2249_51148a1641404be8b2c70f0d6a9c6905~mv2.jpg'),
('Jana Nayagan',            'The final leadership.',                165, 'Political', 'Tamil',   '2025-11-15', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnlzkOimq2QTp4A0Nbet25xwcy0nr2wmVYDg&s'),
('Ponniyin Selvan: I',      'Chola empire struggle.',               167, 'Drama',     'Tamil',   '2022-09-30', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLPg2otOG3aIP21sU4QB3vMKiS2WLHvnjnWQ&s'),
('Avatar: The Way of Water','The sea of Pandora.',                  192, 'Sci-Fi',    'English', '2022-12-16', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_XLR5oupuwYTeLMinLKBwExRrJ4sXzMYd7w&s'),
('Raaka',                   'Allu Arjun in a sci-fi epic.',         180, 'Sci-Fi',    'Telugu',  '2026-04-14', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM3CI1Hy5AKqJwtdRFFvhB9zasmQN61ep-PA&s');

-- =============================================
-- STEP 4: THEATRES
-- =============================================
INSERT INTO THEATRE (name, location, total_screens) VALUES 
('Cinepolis Luxe',   'Forum Mall, Chennai',            8),
('PVR Vegas',        'Dwarka, Delhi',                 12),
('INOX Insignia',    'Phoenix Mall, Mumbai',            6),
('Sathyam Cinemas',  'Royapettah, Chennai',             6),
('SPI Cinemas',      'The Forum Vijaya, Chennai',       8);

-- =============================================
-- STEP 5: SHOWS (future dates)
-- =============================================
INSERT INTO SHOWS (movie_id, theatre_id, show_time, price_base) VALUES 
(1,  1, '2026-05-01 10:00:00', 250.00),   -- The Batman @ Cinepolis
(1,  1, '2026-05-01 14:00:00', 250.00),   -- The Batman @ Cinepolis
(1,  1, '2026-05-01 18:00:00', 300.00),   -- The Batman @ Cinepolis (evening)
(2,  2, '2026-05-01 11:30:00', 200.00),   -- Dune @ PVR Vegas
(3,  3, '2026-05-01 15:45:00', 350.00),   -- Spider-Man @ INOX
(6,  4, '2026-05-01 19:00:00', 280.00),   -- Oppenheimer @ Sathyam
(9,  5, '2026-05-01 22:30:00', 400.00),   -- Leo @ SPI
(10, 2, '2026-05-02 10:00:00', 300.00),   -- RRR @ PVR
(4,  3, '2026-05-02 14:30:00', 220.00),   -- Inception @ INOX
(5,  1, '2026-05-02 17:00:00', 260.00);   -- Interstellar @ Cinepolis

-- =============================================
-- STEP 6: SEATS for Show 1 (The Batman)
-- =============================================
INSERT INTO SEAT (show_id, seat_number, seat_type, price_multiplier) VALUES 
(1, 'A1', 'Silver',   1.00), (1, 'A2', 'Silver',   1.00), (1, 'A3', 'Silver',   1.00),
(1, 'A4', 'Silver',   1.00), (1, 'A5', 'Silver',   1.00),
(1, 'B1', 'Gold',     1.25), (1, 'B2', 'Gold',     1.25), (1, 'B3', 'Gold',     1.25),
(1, 'B4', 'Gold',     1.25), (1, 'B5', 'Gold',     1.25),
(1, 'C1', 'Platinum', 1.50), (1, 'C2', 'Platinum', 1.50), (1, 'C3', 'Platinum', 1.50);

-- Seats for Show 2
INSERT INTO SEAT (show_id, seat_number, seat_type, price_multiplier) VALUES 
(2, 'A1', 'Silver', 1.00), (2, 'A2', 'Silver', 1.00), (2, 'A3', 'Silver', 1.00),
(2, 'B1', 'Gold',   1.25), (2, 'B2', 'Gold',   1.25),
(2, 'C1', 'Platinum', 1.50), (2, 'C2', 'Platinum', 1.50);

-- =============================================
-- STEP 7: CLEAN BOOKINGS (3 Confirmed, 1 Cancelled, 1 Pending)
-- =============================================
INSERT INTO BOOKING (user_id, show_id, total_amount, booking_status) VALUES 
(2, 1, 250.00,  'Confirmed'),   -- John Doe  - The Batman (Silver)
(3, 1, 312.50,  'Confirmed'),   -- Jane Smith - The Batman (Gold)
(4, 1, 375.00,  'Confirmed'),   -- Sridharan  - The Batman (Platinum)
(2, 2, 250.00,  'Confirmed'),   -- John Doe  - The Batman (eve)
(3, 2, 312.50,  'Cancelled');   -- Jane Smith - cancelled

-- =============================================
-- STEP 8: BOOKING SEATS
-- =============================================
INSERT INTO BOOKING_SEAT (booking_id, seat_id) VALUES 
(1, 1),   -- John Doe → A1
(2, 6),   -- Jane Smith → B1
(3, 11),  -- Sridharan → C1
(4, 14);  -- John Doe → A1 of show 2

-- =============================================
-- STEP 9: PAYMENTS
-- =============================================
INSERT INTO PAYMENT (booking_id, amount, payment_method, payment_status) VALUES 
(1, 250.00,  'Credit Card', 'Success'),
(2, 312.50,  'UPI',         'Success'),
(3, 375.00,  'Debit Card',  'Success'),
(4, 250.00,  'Net Banking', 'Success');

-- =============================================
-- VERIFY: Check everything looks correct
-- =============================================
SELECT '=== USERS ===' AS '';
SELECT user_id, name, email, role FROM USERS;

SELECT '=== MOVIES ===' AS '';
SELECT movie_id, title, genre, duration_mins FROM MOVIES;

SELECT '=== THEATRES ===' AS '';
SELECT * FROM THEATRE;

SELECT '=== SHOWS ===' AS '';
SELECT s.show_id, m.title, t.name, s.show_time, s.price_base
FROM SHOWS s JOIN MOVIES m ON s.movie_id=m.movie_id JOIN THEATRE t ON s.theatre_id=t.theatre_id;

SELECT '=== BOOKINGS ===' AS '';
SELECT b.booking_id, u.name, m.title, b.total_amount, b.booking_status
FROM BOOKING b 
JOIN USERS u ON b.user_id=u.user_id
JOIN SHOWS s ON b.show_id=s.show_id
JOIN MOVIES m ON s.movie_id=m.movie_id;

SELECT '=== PAYMENTS ===' AS '';
SELECT * FROM PAYMENT;

SELECT '=== DASHBOARD SUMMARY ===' AS '';
SELECT
  (SELECT COUNT(*) FROM USERS WHERE role='customer')            AS total_customers,
  (SELECT COUNT(*) FROM MOVIES)                                 AS total_movies,
  (SELECT COUNT(*) FROM BOOKING WHERE booking_status='Confirmed') AS confirmed_bookings,
  (SELECT SUM(amount) FROM PAYMENT WHERE payment_status='Success') AS total_revenue;
