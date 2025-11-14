-- Query 1: Detailed Order Information
-- This query joins users, orders, order_items, and products to provide a detailed view of each line item in every order.

SELECT
    u.name AS user_name,
    u.email AS user_email,
    o.order_id,
    o.order_date,
    p.name AS product_name,
    p.category,
    oi.quantity,
    p.price,
    (oi.quantity * p.price) AS line_total
FROM
    users u
JOIN
    orders o ON u.user_id = o.user_id
JOIN
    order_items oi ON o.order_id = oi.order_id
JOIN
    products p ON oi.product_id = p.product_id
ORDER BY
    o.order_date DESC;


-- Query 2: Total Spend Per User
-- This query calculates the total amount spent by each user across all their orders.

SELECT
    u.name AS user_name,
    u.email AS user_email,
    SUM(o.total_amount) AS total_spend
FROM
    users u
JOIN
    orders o ON u.user_id = o.user_id
GROUP BY
    u.user_id, u.name, u.email
ORDER BY
    total_spend DESC;
