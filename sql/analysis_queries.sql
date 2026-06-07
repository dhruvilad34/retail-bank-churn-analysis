-- ============================================================
-- RETAIL BANK CHURN ANALYSIS — SQL QUERIES
-- Analyst : Dhruvi Lad
-- Dataset : 10,000 Canadian Bank Customers
-- Tool    : SQLite
-- ============================================================

-- ── QUERY 1: Overall Business KPIs ──────────────────────────
SELECT
    COUNT(*)                                          AS total_customers,
    SUM(churned)                                      AS total_churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(balance), 2)                            AS avg_balance,
    ROUND(AVG(credit_score), 2)                       AS avg_credit_score,
    ROUND(AVG(satisfaction_score), 2)                 AS avg_satisfaction
FROM customers;

-- ── QUERY 2: Churn Rate by Province ─────────────────────────
SELECT
    province,
    COUNT(*)                                          AS total_customers,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(balance), 2)                            AS avg_balance
FROM customers
GROUP BY province
ORDER BY churn_rate_pct DESC;

-- ── QUERY 3: Churn by Age Band ───────────────────────────────
SELECT
    CASE
        WHEN age < 30              THEN 'Under 30'
        WHEN age BETWEEN 30 AND 44 THEN '30-44'
        WHEN age BETWEEN 45 AND 59 THEN '45-59'
        ELSE '60+'
    END                                               AS age_band,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(balance), 2)                            AS avg_balance
FROM customers
GROUP BY age_band
ORDER BY churn_rate_pct DESC;

-- ── QUERY 4: Churn by Number of Products ────────────────────
SELECT
    num_products,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct
FROM customers
GROUP BY num_products
ORDER BY num_products;

-- ── QUERY 5: Active vs Inactive Member Churn ────────────────
SELECT
    CASE WHEN is_active_member = 1
         THEN 'Active' ELSE 'Inactive' END            AS member_status,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct
FROM customers
GROUP BY is_active_member;

-- ── QUERY 6: Impact of Complaints on Churn ──────────────────
SELECT
    CASE WHEN has_complaint = 1
         THEN 'Has Complaint' ELSE 'No Complaint' END AS complaint_status,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(satisfaction_score), 2)                 AS avg_satisfaction
FROM customers
GROUP BY has_complaint;

-- ── QUERY 7: Churn by Card Type ─────────────────────────────
SELECT
    card_type,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(points_earned), 0)                      AS avg_points,
    ROUND(AVG(satisfaction_score), 2)                 AS avg_satisfaction
FROM customers
GROUP BY card_type
ORDER BY churn_rate_pct DESC;

-- ── QUERY 8: High-Value Customers Who Churned ───────────────
SELECT
    customer_id,
    age,
    province,
    card_type,
    balance,
    num_products,
    satisfaction_score,
    has_complaint
FROM customers
WHERE churned = 1
  AND balance > 100000
ORDER BY balance DESC
LIMIT 20;

-- ── QUERY 9: Satisfaction Score vs Churn ────────────────────
SELECT
    satisfaction_score,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct
FROM customers
GROUP BY satisfaction_score
ORDER BY satisfaction_score;

-- ── QUERY 10: Province + Gender Cross Analysis ───────────────
SELECT
    province,
    gender,
    COUNT(*)                                          AS total,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 2)        AS churn_rate_pct
FROM customers
GROUP BY province, gender
ORDER BY province, churn_rate_pct DESC;
