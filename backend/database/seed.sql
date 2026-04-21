-- CineTick: Restricted Movie List Seed (19 Approved Titles)
USE movie_booking_system;

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

-- 1. Realistic USERS
INSERT INTO USERS (name, email, password_hash, role) VALUES 
('Admin User', 'admin@gmail.com', '$2b$12$y6eZemMQyxbW/gjIe0/BTO/4txZXHMBZapsvrlrYz/ytDnS80tEly', 'admin'),
('John Doe', 'john@example.com', '$2b$12$ieVpH4QnmIr3GpJsVaaLq.944qSO7rLo7j6z.PZXwQgBEZ5J0Xs1G', 'customer'),
('Jane Smith', 'jane@example.com', '$2b$12$ieVpH4QnmIr3GpJsVaaLq.944qSO7rLo7j6z.PZXwQgBEZ5J0Xs1G', 'customer'),
('Sridharan K', 'sridharanak032006@gmail.com', '$2b$12$ieVpH4QnmIr3GpJsVaaLq.944qSO7rLo7j6z.PZXwQgBEZ5J0Xs1G', 'customer');

-- 2. Restructured MOVIE Table (Strictly 19 Titles)
INSERT INTO MOVIES (title, description, duration_mins, genre, language, release_date, poster_url) VALUES 
('The Batman', 'Corruption in Gotham City.', 176, 'Action', 'English', '2022-03-04', 'https://img10.hotstar.com/image/upload/f_auto,q_auto/sources/r1/cms/prod/4142/1776237014142-i'),
('Dune', 'War for the desert planet Arrakis.', 155, 'Sci-Fi', 'English', '2021-10-22', 'https://media.newyorker.com/photos/61772f3f7a6eb9892dafd2c1/master/pass/Park-Dune.jpg'),
('Spider-Man: No Way Home', 'Peter faces multiversal threats.', 148, 'Action', 'English', '2021-12-17', 'https://images.indianexpress.com/2021/11/spider-man-no-way-home-1200-2.jpg'),
('Inception', 'Extracting secrets from dreams.', 148, 'Sci-Fi', 'English', '2010-07-16', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_g6LtC3x4Ddfav_XPzw-iQ_f4MqlPMkYYuQ&s'),
('Interstellar', 'NASA journey to find a new home.', 169, 'Sci-Fi', 'English', '2014-11-07', 'https://m.media-amazon.com/images/I/814E2+pjjzL._AC_SL1500_.jpg'),
('Oppenheimer', 'The enigma of the atomic bomb.', 180, 'Biography', 'English', '2023-07-21', 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/Oppenheimer_%28film%29.jpg/250px-Oppenheimer_%28film%29.jpg'),
('Barbie', 'Stereotypical Barbie crisis.', 114, 'Comedy', 'English', '2023-07-21', 'https://upload.wikimedia.org/wikipedia/en/0/0b/Barbie_2023_poster.jpg'),
('Jailer 2', 'The return of the tiger.', 170, 'Action', 'Tamil', '2025-08-10', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREvB05WGBe19rb24kCGUjudps-H63oIAGfcw&s'),
('Leo', 'A calm before the storm.', 164, 'Action', 'Tamil', '2023-10-19', 'https://images.indianexpress.com/2023/10/leo-review-19102023.jpg'),
('RRR', 'The epic brotherhood.', 187, 'Action', 'Telugu', '2022-03-25', 'https://m.media-amazon.com/images/I/81XSirG7qFL._UF894,1000_QL80_.jpg'),
('Animal', 'Family, blood, and fury.', 201, 'Drama', 'Hindi', '2023-12-01', 'https://m.media-amazon.com/images/M/MV5BZThmNDg1NjUtNWJhMC00YjA3LWJiMjItNmM4ZDQ5ZGZiN2Y2XkEyXkFqcGc@._V1_.jpg'),
('Pushpa: The Rise', 'Sandalwood smuggler.', 179, 'Action', 'Telugu', '2021-12-17', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43EpXkB8hyRy47_DBdbZI3kmLMxn7dJdjOA&s'),
('Vikram', 'The high-octane thriller.', 175, 'Action', 'Tamil', '2022-06-03', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG_4DuNSmYs7fdFTTDdE1TZYwoMYk-RLuNjw&s'),
('Kantara', 'Divine justice.', 148, 'Thriller', 'Kannada', '2022-09-30', 'https://i0.wp.com/ficklesorts.com/wp-content/uploads/2024/04/kantara-featured.jpg?fit=1200%2C675&ssl=1'),
('Varanasi', 'Mahesh Babu in Rajamouli epic.', 175, 'Adventure', 'Hindi', '2026-07-21', 'https://static.wixstatic.com/media/7c2249_51148a1641404be8b2c70f0d6a9c6905~mv2.jpg/v1/fill/w_672,h_448,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/7c2249_51148a1641404be8b2c70f0d6a9c6905~mv2.jpg'),
('Jana Nayagan', 'The final leadership.', 165, 'Political', 'Tamil', '2025-11-15', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnlzkOimq2QTp4A0Nbet25xwcy0nr2wmVYDg&s'),
('Ponniyin Selvan: I', 'Chola empire struggle.', 167, 'Drama', 'Tamil', '2022-09-30', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLPg2otOG3aIP21sU4QB3vMKiS2WLHvnjnWQ&s'),
('Avatar: The Way of Water', 'The sea of Pandora.', 192, 'Sci-Fi', 'English', '2022-12-16', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_XLR5oupuwYTeLMinLKBwExRrJ4sXzMYd7w&s'),
('Raaka', 'Allu Arjun in a sci-fi epic.', 180, 'Sci-Fi', 'Telugu', '2026-04-14', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM3CI1Hy5AKqJwtdRFFvhB9zasmQN61ep-PA&s');

-- 3. Realistic THEATRES
INSERT INTO THEATRE (name, location, total_screens) VALUES 
('Cinepolis Luxe', 'Forum Mall, Chennai', 8),
('PVR Vegas', 'Dwarka, Delhi', 12),
('INOX Insignia', 'Phoenix Mall, Mumbai', 6),
('Sathyam Cinemas', 'Royapettah, Chennai', 6),
('SPI Cinemas', 'The Forum Vijaya, Chennai', 8);

-- 4. Realistic SHOWS (Re-mapped to new IDs)
INSERT INTO SHOWS (movie_id, theatre_id, show_time, price_base) VALUES 
(1, 1, '2026-04-20 10:00:00', 250.00),
(1, 1, '2026-04-20 14:00:00', 250.00),
(1, 1, '2026-04-20 18:00:00', 300.00),
(2, 2, '2026-04-20 11:30:00', 200.00),
(3, 3, '2026-04-20 15:45:00', 350.00),
(6, 4, '2026-04-20 19:00:00', 280.00),
(9, 5, '2026-04-20 22:30:00', 400.00);

-- 5. Realistic SEATS for Show 1 (The Batman)
INSERT INTO SEAT (show_id, seat_number, seat_type, price_multiplier) VALUES 
(1, 'A1', 'Silver', 1.00), (1, 'A2', 'Silver', 1.00), (1, 'A3', 'Silver', 1.00),
(1, 'B1', 'Gold', 1.25), (1, 'B2', 'Gold', 1.25), (1, 'B3', 'Gold', 1.25),
(1, 'C1', 'Platinum', 1.50), (1, 'C2', 'Platinum', 1.50), (1, 'C3', 'Platinum', 1.50);

-- 6. Sample BOOKINGS
INSERT INTO BOOKING (user_id, show_id, total_amount, booking_status) VALUES 
(2, 1, 250.00, 'Confirmed'),
(3, 1, 312.50, 'Confirmed'),
(4, 1, 375.00, 'Confirmed');

-- 7. Sample BOOKING_SEATS
INSERT INTO BOOKING_SEAT (booking_id, seat_id) VALUES 
(1, 1), (2, 4), (3, 7);

-- 8. Sample PAYMENTS
INSERT INTO PAYMENT (booking_id, amount, payment_method, payment_status) VALUES 
(1, 250.00, 'Credit Card', 'Success'),
(2, 312.50, 'UPI', 'Success'),
(3, 375.00, 'Debit Card', 'Success');
