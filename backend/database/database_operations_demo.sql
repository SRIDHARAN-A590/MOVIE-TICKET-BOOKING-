-- CineTick: Database Operations & Query Demo Script
-- This script demonstrates all mandatory SQL concepts (Joins, Subqueries, Aggregation, optimization, etc.)

USE movie_booking_system;

-- =============================================
-- 3 & 4. SQL QUERIES & JOINS (Requirements 3 & 4)
-- =============================================

-- Example 1: INNER JOIN - Fetch complete booking details for all users
-- This combines 4 tables to show a human-readable booking history
SELECT 
    b.booking_id,
    u.name AS user_name,
    m.title AS movie_title,
    t.name AS theatre_name,
    s.show_time,
    b.total_amount
FROM BOOKING b
INNER JOIN USERS u ON b.user_id = u.user_id
INNER JOIN SHOWS s ON b.show_id = s.show_id
INNER JOIN MOVIES m ON s.movie_id = m.movie_id
INNER JOIN THEATRE t ON s.theatre_id = t.theatre_id
ORDER BY s.show_time DESC;

-- Example 2: LEFT JOIN - Fetch all movies and their booking counts (including movies with 0 bookings)
SELECT 
    m.title,
    COUNT(b.booking_id) AS total_bookings
FROM MOVIES m
LEFT JOIN SHOWS s ON m.movie_id = s.movie_id
LEFT JOIN BOOKING b ON s.show_id = b.show_id
GROUP BY m.title
ORDER BY total_bookings DESC;

-- =============================================
-- 5. SUBQUERIES (Requirement 5)
-- =============================================

-- Example 1: Finding available seats for 'The Batman' using a subquery
SELECT seat_number, seat_type
FROM SEAT
WHERE show_id = (SELECT show_id FROM SHOWS WHERE movie_id = (SELECT movie_id FROM MOVIES WHERE title = 'The Batman' LIMIT 1) LIMIT 1)
AND status = 'Available';

-- Example 2: Fetching users who have booked more than the average booking amount
SELECT name, email
FROM USERS
WHERE user_id IN (
    SELECT user_id 
    FROM BOOKING 
    WHERE total_amount > (SELECT AVG(total_amount) FROM BOOKING)
);

-- =============================================
-- 3. AGGREGATE FUNCTIONS & HAVING (Requirement 3)
-- =============================================

-- Fetch theatres that have generated more than 500 in total revenue
SELECT 
    t.name AS theatre_name,
    SUM(b.total_amount) AS theatre_revenue
FROM THEATRE t
JOIN SHOWS s ON t.theatre_id = s.theatre_id
JOIN BOOKING b ON s.show_id = b.show_id
GROUP BY t.name
HAVING theatre_revenue > 500;

-- =============================================
-- 7. SQL FUNCTIONS (Date & String) (Requirement 7)
-- =============================================

-- Formatting booking time and combining user details for a CRM report
SELECT 
    UPPER(CONCAT(u.name, ' <', u.email, '>')) AS user_contact_info,
    DATE_FORMAT(b.created_at, '%D %M %Y at %l:%i %p') AS readable_booking_date,
    LENGTH(m.description) AS description_char_count
FROM BOOKING b
JOIN USERS u ON b.user_id = u.user_id
JOIN SHOWS s ON b.show_id = s.show_id
JOIN MOVIES m ON s.movie_id = m.movie_id;

-- =============================================
-- 6. VIEW USAGE (Requirement 6)
-- =============================================

-- Fetch the pre-calculated Movie Revenue Report
SELECT * FROM View_Movie_Revenue_Report;

-- =============================================
-- 10. STORED PROCEDURE & CURSOR EXECUTION (Requirement 10 & 12)
-- =============================================

-- Display available seats for Show 1 using our cursor-based procedure
CALL Proc_Display_Available_Seats(1);

-- =============================================
-- 2. DML EXAMPLES (Requirement 2)
-- =============================================

-- Update: Change the base price of a show
UPDATE SHOWS SET price_base = 350.00 WHERE show_id = 1;

-- Delete: Remove a failed payment record (Example)
DELETE FROM PAYMENT WHERE payment_status = 'Failed' AND payment_time < NOW() - INTERVAL 1 DAY;
