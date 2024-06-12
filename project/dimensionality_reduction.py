import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import FactorAnalyzer

# CSV ფაილების წაკითხვა
employees = pd.read_csv('employees.csv')
satisfaction_surveys = pd.read_csv('satisfaction_surveys.csv')
motivation_surveys = pd.read_csv('motivation_surveys.csv')

# მონაცემთა გაერთიანება თანამშრომელთა ID-ებზე
merged_data = pd.merge(satisfaction_surveys, motivation_surveys, on='employee_id', suffixes=('_satisfaction', '_motivation'))
merged_data = pd.merge(merged_data, employees, on='employee_id')

# სვეტების ამორჩევა
data_for_analysis = merged_data[['satisfaction_level', 'motivation_level']]

# მონაცემთა სკალირება
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_for_analysis)

# PCA გამოყენება
pca = PCA(n_components=2)
pca_components = pca.fit_transform(scaled_data)

# PCA შედეგების პლოტირება
plt.figure(figsize=(8, 6))
plt.scatter(pca_components[:, 0], pca_components[:, 1])
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.title('PCA Results')
plt.show()

# Explained variance plot
explained_variance = pca.explained_variance_ratio_
plt.figure(figsize=(8, 6))
plt.bar(range(len(explained_variance)), explained_variance)
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.title('Explained Variance by Principal Components')
plt.show()

# ფაქტორული ანალიზის გამოყენება
fa = FactorAnalyzer(n_factors=2, rotation='varimax')
fa.fit(scaled_data)

# ფაკტორული დატვირთვის მატრიცის მიღება
factor_loadings = fa.loadings_

# ფაქტორული ანალიზის შედეგების პლოტირება
plt.figure(figsize=(8, 6))
sns.heatmap(factor_loadings, annot=True, cmap='viridis')
plt.xlabel('Factors')
plt.ylabel('Variables')
plt.title('Factor Analysis Loadings')
plt.show()

# ჰისტოგრამების აგება კმაყოფილების და მოტივაციისთვის
plt.figure(figsize=(8, 6))
sns.histplot(merged_data['satisfaction_level'], kde=True, color='blue', label='Satisfaction')
sns.histplot(merged_data['motivation_level'], kde=True, color='green', label='Motivation')
plt.legend()
plt.title('Satisfaction and Motivation Levels Distribution')
plt.xlabel('Level')
plt.ylabel('Frequency')
plt.show()

# შეჯამებული ინფორმაცია PCA-სა და ფაქტორული ანალიზის შესახებ
print("PCA Explained Variance Ratios:", explained_variance)
print("\nFactor Analysis Loadings:\n", factor_loadings)
