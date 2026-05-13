import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import openpyxl

filepath = r"C:/Users/Aryaman Gupta/Desktop/KDP Pay.xlsx"
df = pd.read_excel(filepath, header=None)

df.replace(np.nan, 0.0, inplace=True)
df.columns = df.iloc[0]
df_new = df.drop(index=0).reset_index(drop=True)

df_group = df_new[['Marketplace', 'Net Earnings', 'Source']]
grouped = df_group.pivot_table(index='Marketplace', columns='Source', values='Net Earnings', aggfunc='sum')
# Inside your plotting code, after `grouped.plot(...)`:

ax = grouped.plot(
    kind='bar',
    figsize=(10, 6),
    stacked=False,
    colormap='tab20'
)

plt.title("Net Earnings by Marketplace and Source")
plt.ylabel("Net Earnings")
plt.xlabel("Marketplace")
plt.xticks(rotation=45)
plt.legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')

# === Use annotate to label bars ===
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        if height > 0:
            ax.annotate(
                f'{height:.2f}',                     # Text label
                xy=(bar.get_x() + bar.get_width() / 2, height),  # Position (x, y)
                xytext=(0, 3),                        # Offset (0 horiz, 3 pts up)
                textcoords="offset points",           # Use offset in points
                ha='center', va='bottom',
                fontsize=8
            )

plt.tight_layout()
plt.show()

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
import seaborn as sns

print(df_new.head())

df_new[['Payment Number','Accrued Royalty','Tax Withholding','Net Earnings','FX Rate','Payout Amount']] = df_new[['Payment Number','Accrued Royalty','Tax Withholding','Net Earnings','FX Rate','Payout Amount']].astype('float')
print(df_new.info())
sns.regplot(x="Accrued Royalty",y="Payout Amount", data=df_new, line_kws={"color":"red"})
plt.ylim(0,)
plt.show() ##########################Plot shows a strong linear relationship - As Royalty increases, the payout amount also increases
print(df_new["Currency"].iloc[:, 0].value_counts())
# Remove duplicate column names
df_new = df_new.loc[:, ~df_new.columns.duplicated()]
dummy_variable_1 = pd.get_dummies(df_new["Currency"])
print(dummy_variable_1.head())
# merge data frame "df_new" and "dummy_variable_1" 
df_new = pd.concat([df_new, dummy_variable_1], axis=1)

# drop original column "fuel-type" from "df_new"
df_new.drop("Currency", axis = 1, inplace=True)
df_new[['GBP','INR','USD']]=df_new[['GBP','INR','USD']].astype('int')
print(df_new.info())
print(df_new.head())
# Reconstruct 'Currency' column from dummy variables
df_new['Currency'] = df_new[['GBP', 'INR', 'USD']].idxmax(axis=1) #Deconstructing currency and again reconstructing it becomes redundant..
#here it is done for training purpose only

sns.boxplot(x='Currency', y='Tax Withholding', data=df_new)
plt.title("Tax Withholding by Currency")
plt.ylabel('Amount')
plt.ylim(0, 15)
plt.grid(True)
plt.show()