import pandas as pd

# ── 1. Load raw data ──────────────────────────────────────────
df = pd.read_csv('data/Customer-Churn-Records.csv')

print("=" * 50)
print("RAW DATA OVERVIEW")
print("=" * 50)
print(f"Shape        : {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"\nMissing values:\n{df.isnull().sum()}")

# ── 2. Canadianize Geography ──────────────────────────────────
province_map = {
    'France':  'Ontario',
    'Germany': 'British Columbia',
    'Spain':   'Quebec'
}
df['Geography'] = df['Geography'].replace(province_map)

# ── 3. Rename columns ─────────────────────────────────────────
df.rename(columns={
    'RowNumber':          'row_number',
    'CustomerId':         'customer_id',
    'Surname':            'surname',
    'CreditScore':        'credit_score',
    'Geography':          'province',
    'Gender':             'gender',
    'Age':                'age',
    'Tenure':             'tenure_years',
    'Balance':            'balance',
    'NumOfProducts':      'num_products',
    'HasCrCard':          'has_credit_card',
    'IsActiveMember':     'is_active_member',
    'EstimatedSalary':    'estimated_salary',
    'Exited':             'churned',
    'Complain':           'has_complaint',
    'Satisfaction Score': 'satisfaction_score',
    'Card Type':          'card_type',
    'Point Earned':       'points_earned'
}, inplace=True)

# ── 4. Clean up ───────────────────────────────────────────────
df.drop(columns=['row_number'], inplace=True)
df['card_type'] = df['card_type'].str.title()

# ── 5. Save ───────────────────────────────────────────────────
df.to_csv('data/bank_customers_clean.csv', index=False)

print("\n" + "=" * 50)
print("CLEANED DATA SUMMARY")
print("=" * 50)
print(f"Shape              : {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Columns            : {list(df.columns)}")
print(f"\nProvince distribution:\n{df['province'].value_counts()}")
print(f"\nChurn rate         : {df['churned'].mean():.1%}")
print(f"Complaint rate     : {df['has_complaint'].mean():.1%}")
print(f"Avg satisfaction   : {df['satisfaction_score'].mean():.2f} / 5.0")
print(f"Card types         :\n{df['card_type'].value_counts()}")
print(f"\nAvg balance (churned)  : ${df[df['churned']==1]['balance'].mean():,.2f}")
print(f"Avg balance (retained) : ${df[df['churned']==0]['balance'].mean():,.2f}")
print("\n✅ Saved to data/bank_customers_clean.csv")
