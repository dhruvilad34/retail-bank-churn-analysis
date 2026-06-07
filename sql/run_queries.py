import sqlite3
import pandas as pd
import os

conn = sqlite3.connect('data/bank_churn.db')
os.makedirs('data/query_results', exist_ok=True)

queries = {
    "01_overall_kpis": """
        SELECT COUNT(*) AS total_customers, SUM(churned) AS total_churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct,
               ROUND(AVG(balance),2) AS avg_balance,
               ROUND(AVG(satisfaction_score),2) AS avg_satisfaction
        FROM customers""",

    "02_churn_by_province": """
        SELECT province, COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct,
               ROUND(AVG(balance),2) AS avg_balance
        FROM customers GROUP BY province ORDER BY churn_rate_pct DESC""",

    "03_churn_by_age_band": """
        SELECT CASE WHEN age<30 THEN 'Under 30'
                    WHEN age BETWEEN 30 AND 44 THEN '30-44'
                    WHEN age BETWEEN 45 AND 59 THEN '45-59'
                    ELSE '60+' END AS age_band,
               COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY age_band ORDER BY churn_rate_pct DESC""",

    "04_churn_by_products": """
        SELECT num_products, COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY num_products ORDER BY num_products""",

    "05_active_vs_inactive": """
        SELECT CASE WHEN is_active_member=1 THEN 'Active' ELSE 'Inactive' END AS member_status,
               COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY is_active_member""",

    "06_complaint_impact": """
        SELECT CASE WHEN has_complaint=1 THEN 'Has Complaint' ELSE 'No Complaint' END AS complaint_status,
               COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct,
               ROUND(AVG(satisfaction_score),2) AS avg_satisfaction
        FROM customers GROUP BY has_complaint""",

    "07_churn_by_card_type": """
        SELECT card_type, COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct,
               ROUND(AVG(points_earned),0) AS avg_points
        FROM customers GROUP BY card_type ORDER BY churn_rate_pct DESC""",

    "08_high_value_churned": """
        SELECT customer_id, age, province, card_type, balance,
               num_products, satisfaction_score, has_complaint
        FROM customers WHERE churned=1 AND balance>100000
        ORDER BY balance DESC LIMIT 20""",

    "09_satisfaction_vs_churn": """
        SELECT satisfaction_score, COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY satisfaction_score ORDER BY satisfaction_score""",

    "10_province_gender": """
        SELECT province, gender, COUNT(*) AS total, SUM(churned) AS churned,
               ROUND(100.0*SUM(churned)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY province, gender ORDER BY province, churn_rate_pct DESC"""
}

print("=" * 60)
print("RUNNING ALL SQL QUERIES")
print("=" * 60)

for name, query in queries.items():
    df = pd.read_sql_query(query, conn)
    df.to_csv(f'data/query_results/{name}.csv', index=False)
    print(f"\n📊 {name}:")
    print(df.to_string(index=False))

conn.close()
print("\n" + "=" * 60)
print("✅ All query results saved to data/query_results/")
print("=" * 60)
