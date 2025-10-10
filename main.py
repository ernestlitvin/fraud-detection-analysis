import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from pandas import value_counts

df = pd.read_csv("credit_card_fraud_2025.csv")
# df.info()
df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"])
df.info()
df_describe = df.describe()
# print(f"\n {df_describe}")
duplicates_count = df.duplicated().sum()
print(f"\nFound {duplicates_count} duplicates")
df = df.drop_duplicates()
df.columns = [col.lower() for col in df.columns]
print(f"\nLeft duplicates: {df.duplicated().sum()}")
min_date = df["transaction_date"].min()
print(f"\nMin date: {min_date}")
max_date = df["transaction_date"].max()
print(f"\nMax date: {max_date}")
card_types = df["card_type"].value_counts()
print(f"\n{card_types}")
transaction_types = df["transaction_type"].value_counts()
print(f"\n{transaction_types}")
merchant_categories = df["merchant_category"].value_counts()
print(f"\n{merchant_categories}")
counties = df["country"].value_counts()
print(f"\n{counties}")
sns.histplot(df["amount"])
plt.show()

# Hypothesis 1: The fraud cases are very common act.
# How often is fraud encountered? (What percentage of transactions are fraudulent?)
fraud_counts = df["fraud_flag"].value_counts()[1] # fraud_counts = len(df[df["fraud_flag"] == 1])
transactions_count = df["transaction_id"].count() # transactions_count = len(df["transaction_id"])
fraud_prt = fraud_counts / transactions_count * 100
print(f"\n Fraud was encountered: {fraud_counts} times in {transactions_count} transactions ")
print(f"\n Fraud percentage: {fraud_prt} % ")
# Hypothesis 2: Fraud cases are move made on big amounts.
# Are the amounts of fraudulent and ordinary transactions different?
# (Compare Amount statistics for two groups: Fraud_Flag = 0 and Fraud_Flag = 1).
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
fraud_type_dif = df.groupby("fraud_flag")['amount'].describe()
print(fraud_type_dif)

sns.histplot(data = df, x="amount", hue = "fraud_flag", stat = "density", common_norm=False)
ax = plt.gca()
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
plt.show()

df_filtered = df[df["amount"] < 300]
sns.boxplot(data=df_filtered, x = "fraud_flag", y = "amount")
plt.show()

df_filtered_by_amount = df[df["amount"] < 300]
sns.displot(data = df_filtered_by_amount, x = "amount", col = "fraud_flag")
plt.suptitle("Distribution of sums", y=1.02)
plt.show()

# Hypothesis 3: Does the pattern of fraud distribution by hours differ from the pattern of normal transactions?

fraud_df = df[df["fraud_flag"] == 1] ## fraud_percents = df[df['fraud_flag'] == 1]['hour_of_day'].value_counts(normalize=True).sort_index()
fraud_df_by_hours = fraud_df["hour_of_day"].value_counts(normalize=True).sort_index() ##
non_fraud_df = df[df["fraud_flag"] == 0] ## non_fraud_percents = df[df['fraud_flag'] == 0]['hour_of_day'].value_counts(normalize=True).sort_index()
non_fraud_df_by_hours = non_fraud_df["hour_of_day"].value_counts(normalize=True).sort_index()
# alternative # 1
# hourly_distribution = df.groupby('fraud_flag')['hour_of_day'].value_counts(normalize=True)
# print(hourly_distribution)
# alternative # 2
# cross_table = pd.crosstab(index=df['hour_of_day'],
#                           columns=df['fraud_flag'],
#                           normalize='columns')
# print(cross_table)

plt.figure(figsize=(12, 6))
sns.lineplot(x =fraud_df_by_hours.index, y = fraud_df_by_hours.values, label = "Fraud transactions") ## sns.lineplot(data = fraud_df_by_hours)
sns.lineplot(x =non_fraud_df_by_hours.index, y = non_fraud_df_by_hours.values, label = "Non-fraud transactions") ## sns.lineplot(data = non_fraud_df_by_hours)
plt.title("Percentage distribution of transactions by time")
plt.xlabel("Hour of Day")
plt.ylabel("Share of transactions in groups (%)")
plt.xticks(range(0, 24))
plt.legend()
plt.grid(True)
plt.show()

# Hypothesis 4: Are there any product categories (merchant_category) that have a higher risk of fraud than others?

fraud_label = {0 : "Non-fraud",
                1 : "Fraud"}
df["fraud_label"] = df["fraud_flag"].map(fraud_label)

merchant_cat_dist = df.groupby("fraud_label")["merchant_category"].value_counts(normalize=True).reset_index()

merchant_cross_table = pd.crosstab(index=df['merchant_category'],
                          columns=df['fraud_label'],
                          normalize='columns',)
merchant_cross_table["risk_factor"] = merchant_cross_table["Fraud"] / merchant_cross_table["Non-fraud"]
merchant_cross_table_sort = merchant_cross_table.sort_values(by = "risk_factor", ascending=False)
# print(f"\n{merchant_cross_table_sort}")

plt.figure(figsize=(11, 5))
sns.barplot(data = merchant_cat_dist, x = "merchant_category", y = "proportion", hue = "fraud_label")
plt.xlabel("Merchant Category")
plt.ylabel("Proportion (%)")
plt.xticks(rotation=20)
plt.legend(loc="lower right")
plt.grid(True)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()

def time_day(hour):
    if 0 <= hour < 6:
        return "Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Day"
    else:
        return "Evening"

df["time_of_day"] = df["hour_of_day"].apply(time_day)

fraud_dist_by_time_day = df.groupby("fraud_label")["time_of_day"].value_counts(normalize=True).reset_index()
sns.barplot(data = fraud_dist_by_time_day, x = "time_of_day", y = "proportion", hue = "fraud_label")
plt.show()


# # Анализ мошеннических транзакций по кредитным картам
#
## 1. Цель проекта
Цель проекта - проанализировать поведение мошеников при использовании карты:
- Связаны ли акты мошеничества с суммой (чем больше сумма - тем большая вероятность мошеничества);
- Проверить в какое время (суток) происходит акт мошеничества;
- Какие категории товаров более подвергнуты к мошеническим актам.

## 2. Источник данных
https://www.kaggle.com/datasets/prince7489/credit-card-fraud-2025

## 3. Ключевые выводы
1. Не наблюдается паттернов сум при мошенических операциях и при обычных транзакциях.
2. Ночь — самое рискованное время. Ночью доля мошеннических транзакций непропорционально выше, чем доля обычных.
Вечером ситуация обратная, а утром и днем паттерны слабо отличаются (идентичны). Пики мошеничества в 12 часов ночи, и 5 часов утра, когда обычные транзакции просиходят на одном уровне в течении круглых суток.
3. Больше всего мошенические акты происходят в категориях: онлайн покупок, бижутерии, путешествия.
Менеьше всего - еда, одежда.

## 4. Использованные инструменты
(Python, Pandas, Seaborn, Matplotlib)


