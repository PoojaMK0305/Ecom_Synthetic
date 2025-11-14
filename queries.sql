-- queries.sql
-- For each order return: order_id, order_date, user_id, user_name, total_amount, item_count, top_product_name
SELECT
  o.order_id,
  o.order_date,
  u.user_id,
  u.name AS user_name,
  o.total_amount,
  COUNT(oi.item_id) AS item_count,
  (
    SELECT p.name
    FROM order_items oi2
    JOIN products p ON p.product_id = oi2.product_id
    WHERE oi2.order_id = o.order_id
    ORDER BY oi2.line_total DESC
    LIMIT 1
  ) AS top_product_name
FROM orders o
JOIN users u ON u.user_id = o.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.order_date, u.user_id, u.name, o.total_amount
ORDER BY o.total_amount DESC
LIMIT 50;
