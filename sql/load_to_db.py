import pandas as pd
import sqlite3

df = pd.read_csv('data/bank_customers_clean.csv')
conn = sqlite3.connect('data/bank_churn.db')
df.to_sql('customers', conn, if_exists='replace', index=False)

print(f"   Database created: data/bank_churn.db")
print(f"   Table: customers")
print(f"   Rows : {len(df):,}")
print(f"   Cols : {len(df.columns)}")
conn.close()
