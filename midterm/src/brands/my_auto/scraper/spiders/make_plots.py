import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("predicted_prices.csv")


# Scatter plot of Manufacturer vs Predicted Price
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x='Manufacturer', y='Predicted Price', hue='Model', palette='viridis')
plt.title('Manufacturer vs Predicted Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Histogram of Predicted Prices
plt.figure(figsize=(10, 6))
sns.histplot(df['Predicted Price'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Predicted Prices')
plt.xlabel('Predicted Price')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Box plot of Manufacturer vs Predicted Price
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Manufacturer', y='Predicted Price', palette='pastel')
plt.title('Manufacturer vs Predicted Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
