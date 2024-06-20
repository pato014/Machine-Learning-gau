import json
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

file_path_old = 'P1_old.jsonl'
file_path_new = 'P1_new.jsonl'

data_old = []
with open(file_path_old, 'r') as file:
    for line in file:
        data_old.append(json.loads(line))

data_new = []
with open(file_path_new, 'r') as file:
    for line in file:
        data_new.append(json.loads(line))

# მონაცემების DataFrame-ში კონვერტაცია
df_old = pd.DataFrame(data_old)
df_new = pd.DataFrame(data_new)

# პროდუქციის ID-ის და ფასის გამოყოფა
df_old = df_old[['id', 'sellers']].rename(columns={'sellers': 'old_price'})
df_old['old_price'] = df_old['old_price'].apply(lambda x: list(x['values'].values())[0]['amount'] if x['values'] else 0)

df_new = df_new[['id', 'sellers']].rename(columns={'sellers': 'new_price'})
df_new['new_price'] = df_new['new_price'].apply(lambda x: list(x['values'].values())[0]['amount'] if x['values'] else 0)

# მონაცემების გაერთიანება ID-ის მიხედვით
df_combined = pd.merge(df_old, df_new, on='id')

# K-საშუალო მოდელი
features = ['old_price', 'new_price']
kmeans = KMeans(n_clusters=3, random_state=0).fit(df_combined[features])
centroids = kmeans.cluster_centers_
df_combined['cluster'] = kmeans.labels_

# K-NN მოდელი
def get_price_change(old, new):
    if new > old:
        return 'price_increased'
    elif new < old:
        return 'price_decreased'
    else:
        return 'price_unchanged'

df_combined['price_change'] = df_combined.apply(lambda row: get_price_change(row['old_price'], row['new_price']), axis=1)
X = df_combined[features]
y = df_combined['price_change']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

# შეფასების შედეგები
classification_report_str = classification_report(y_test, y_pred)
print(classification_report_str)

# გრაფიკების აგება

# K-Means Clustering
plt.figure(figsize=(10, 6))
plt.scatter(df_combined['old_price'], df_combined['new_price'], c=df_combined['cluster'], cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x')
plt.xlabel('Old Price')
plt.ylabel('New Price')
plt.title('K-Means Clustering')
plt.savefig('kmeans_clustering.png')
plt.show()

# K-Means Centroids
plt.figure(figsize=(10, 6))
plt.bar(range(len(centroids)), centroids[:, 0], alpha=0.5, label='Old Price')
plt.bar(range(len(centroids)), centroids[:, 1], alpha=0.5, label='New Price')
plt.xlabel('Cluster')
plt.ylabel('Price')
plt.title('K-Means Centroids')
plt.legend()
plt.savefig('kmeans_centroids.png')
plt.show()

# K-NN Confusion Matrix
plt.figure(figsize=(10, 6))
ConfusionMatrixDisplay.from_estimator(knn, X_test_scaled, y_test, cmap='Blues')
plt.title('K-NN Confusion Matrix')
plt.savefig('knn_confusion_matrix.png')
plt.show()

# K-NN Classification Results
plt.figure(figsize=(10, 6))
sns.histplot(df_combined['price_change'], kde=False, stat='density', alpha=0.5, label='Actual')
sns.histplot(y_pred, kde=False, stat='density', alpha=0.5, color='red', label='Predicted')
plt.xlabel('Price Change')
plt.ylabel('Density')
plt.title('K-NN Classification Results')
plt.legend()
plt.savefig('knn_classification_results.png')
plt.show()
