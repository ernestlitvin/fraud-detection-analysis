# Credit Card Fraud Transaction Analysis

## 1. Project Goal

The primary goal of this project is to perform an Exploratory Data Analysis (EDA) on a credit card transaction dataset. The objective is to identify key features and patterns that distinguish fraudulent transactions from legitimate ones.

**Main Hypotheses Tested:**
- Is there a correlation between the transaction `Amount` and the likelihood of fraud?
- Are there specific temporal patterns (e.g., time of day) associated with fraudulent activities?
- Do certain `Merchant_Category` entries show a higher risk of fraud?

## 2. Data Source

- **Credit Card Fraud 2025 Dataset:** [https://www.kaggle.com/datasets/prince7489/credit-card-fraud-2025](https://www.kaggle.com/datasets/prince7489/credit-card-fraud-2025)

## 3. Key Findings & Insights

1.  **Transaction `Amount` is a Weak Indicator of Fraud.**
    - The distribution of transaction amounts for the majority of fraudulent and legitimate operations is very similar. This suggests that fraudsters effectively disguise their activities as typical, low-value purchases to avoid immediate suspicion.
![Distribution of Transaction Amounts up to 300](images/dist.png) 

2.  **Time of Day (`Hour_of_Day`) is a VERY STRONG Indicator of Fraud.**
    - A clear pattern was discovered: the proportion of fraudulent transactions is **disproportionately high during the night** (especially between 00:00 and 06:00 AM). In contrast, the activity of legitimate users is minimal at this time. This strongly suggests that fraudsters prefer to operate when victims are most likely asleep and unable to react quickly.
![Proportion of Transactions by Hour (within each group)](images/prop.png) 

3.  **`Merchant_Category` is a Weak but Noticeable Indicator.**
    - Categories such as `Online Services`, `Travel` and `Groceries` exhibit a **disproportionately higher share** of fraudulent transactions compared to their share in legitimate transactions. This marks them as higher-risk categories that may require closer monitoring by fraud detection systems.
![Proportion of Transactions by Category](images/prop_by_cat.png) 

## 4. Tools Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=seaborn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=matplotlib&logoColor=white)
