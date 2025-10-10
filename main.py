# =============================================================================
# === 1. LIBRARY IMPORTS ===
# =============================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =============================================================================
# === 2. DATA LOADING & PREPARATION ===
# =============================================================================
# Load the dataset
df = pd.read_csv("credit_card_fraud_2025.csv")

# --- Data Cleaning & Transformation ---
# Standardize column names to a consistent style (lowercase)
df.columns = [col.lower() for col in df.columns]

# Convert the transaction_date column to datetime format
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# Check for and remove duplicate rows
print(f"Duplicates found: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Duplicates left: {df.duplicated().sum()}\n")

# Create a column with human-readable labels for the fraud flag
fraud_label_map = {0: "Non-Fraud", 1: "Fraud"}
df["fraud_label"] = df["fraud_flag"].map(fraud_label_map)

# Create a column for the part of the day
def get_time_of_day(hour):
    if 0 <= hour < 6:
        return "Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Day"
    else:
        return "Evening"
df["time_of_day"] = df["hour_of_day"].apply(get_time_of_day)

# --- Initial Data Inspection ---
print("--- General Data Information ---")
df.info()
print("\n--- Statistics for Numerical Columns ---")
print(df.describe())
print("\n")

# ==================================================================================
# === 3. EXPLORATORY DATA ANALYSIS (EDA) ===
# ==================================================================================

# --- Hypothesis 1: How imbalanced is the data? ---
fraud_percentage = df["fraud_flag"].value_counts(normalize=True)[1] * 100
print(f"Percentage of fraudulent transactions: {fraud_percentage:.2f}%\n")

# --- Hypothesis 2: Is the transaction amount a strong indicator of fraud? ---
print("--- Comparison of statistics by transaction amount ---")
print(df.groupby("fraud_label")['amount'].describe())

# Visualization of the amount distribution (filtered)
df_filtered = df[df["amount"] < 300]
sns.displot(data=df_filtered, x='amount', col="fraud_label", common_norm=False, kde=True)
plt.suptitle("Distribution of Transaction Amounts up to 300 (Comparison)", y=1)
plt.show()
# Conclusion: The distributions are very similar. Amount is a weak indicator.

# --- Hypothesis 3: Is the time of day a strong indicator of fraud? ---
# Prepare data for the plot (percentage distribution by hour for each group)
fraud_percents_by_hour = df[df['fraud_flag'] == 1]['hour_of_day'].value_counts(normalize=True).sort_index()
non_fraud_percents_by_hour = df[df['fraud_flag'] == 0]['hour_of_day'].value_counts(normalize=True).sort_index()

# Create the plot
plt.figure(figsize=(12, 6))
sns.lineplot(x=fraud_percents_by_hour.index, y=fraud_percents_by_hour.values, label="Fraud")
sns.lineplot(x=non_fraud_percents_by_hour.index, y=non_fraud_percents_by_hour.values, label="Non-Fraud")
plt.title("Proportion of Transactions by Hour (within each group)")
plt.xlabel("Hour of Day")
plt.ylabel("Proportion of Transactions (%)")
plt.xticks(range(0, 24))
plt.legend()
plt.grid(True)
plt.show()
# Conclusion: The patterns are very different. Time of day is a strong indicator.

# --- Hypothesis 4: Are there merchant categories with a higher risk of fraud? ---
# Create a table with a risk factor
cross_table = pd.crosstab(index=df['merchant_category'], columns=df['fraud_label'], normalize='columns')
cross_table['risk_factor'] = cross_table['Fraud'] / cross_table['Non-Fraud']
print("\n--- Categories with the Highest Risk Factor ---")
print(cross_table.sort_values(by='risk_factor', ascending=False))

# Visualization
fraud_dist_by_cat = df.groupby("fraud_label")["merchant_category"].value_counts(normalize=True).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(data=fraud_dist_by_cat, x="merchant_category", y="proportion", hue="fraud_label")
plt.title("Proportion of Transactions by Category")
plt.xlabel("Merchant Category")
plt.ylabel("Proportion (%)")
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()
# Conclusion: There are categories with elevated risk, but the signal is weaker than for time of day.



