import pandas as pd
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error

new_data = []
with open('data.jsonl', 'r') as file:
    for line in file:
        new_data.append(json.loads(line))

df = pd.DataFrame(new_data)




# საჭიროების შემთხვევაში მონაცემების დამუშავება
# გამოსარჩევად სვეტების დასახელებები
target_column = 'price'
feature_columns = ['brand']

# მონაცემების გამოყოფა მახასიათებლებად (X) და სამიზნედ (y)
X = df[feature_columns]
y = df[target_column]

# კატეგორიული სვეტების Dummy სვეტებად გარდაქმნა
X = pd.get_dummies(X, drop_first=True)

# მონაცემთა გაყოფა სასწავლო და სატესტო სეტებად
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# მარყუჟოვანი რეგრესიის მოდელის ტრენინგი
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)

# გრეხილი რეგრესიის მოდელის ტრენინგი
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)

# მოდელის შედეგების შეფასება
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
mse_lasso = mean_squared_error(y_test, y_pred_lasso)

print("Ridge Regression MSE:", mse_ridge)
print("Lasso Regression MSE:", mse_lasso)

plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=30, kde=True)
plt.title('ფასების განაწილების ჰისტოგრამა')
plt.xlabel('ფასი')
plt.ylabel('სიხშირე')
plt.show()

# 2. ფაქტიური vs პროგნოზირებული ფასები მარყუჟოვანი რეგრესიისთვის
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_ridge, color='blue', label='Ridge')
plt.plot([y.min(), y.max()], [y.min(), y.max()], '--r', linewidth=2)
plt.xlabel('ფაქტიური ფასები')
plt.ylabel('პროგნოზირებული ფასები')
plt.title('ფაქტიური vs პროგნოზირებული ფასები (Ridge)')
plt.legend()
plt.show()

# 3. ფაქტიური vs პროგნოზირებული ფასები გრეხილი რეგრესიისთვის
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_lasso, color='green', label='Lasso')
plt.plot([y.min(), y.max()], [y.min(), y.max()], '--r', linewidth=2)
plt.xlabel('ფაქტიური ფასები')
plt.ylabel('პროგნოზირებული ფასები')
plt.title('ფაქტიური vs პროგნოზირებული ფასები (Lasso)')
plt.legend()
plt.show()

# 4. სასჯელის პარამეტრის გავლენა Ridge რეგრესიის კოეფიციენტებზე
alphas = np.logspace(-6, 6, 200)
coefs_ridge = []
for a in alphas:
    ridge = Ridge(alpha=a)
    ridge.fit(X_train, y_train)
    coefs_ridge.append(ridge.coef_)

plt.figure(figsize=(10, 6))
plt.plot(alphas, coefs_ridge)
plt.xscale('log')
plt.xlabel('alpha')
plt.ylabel('კოეფიციენტები')
plt.title('სასჯელის პარამეტრის გავლენა Ridge რეგრესიის კოეფიციენტებზე')
plt.show()

# 5. სასჯელის პარამეტრის გავლენა Lasso რეგრესიის კოეფიციენტებზე
coefs_lasso = []
for a in alphas:
    lasso = Lasso(alpha=a)
    lasso.fit(X_train, y_train)
    coefs_lasso.append(lasso.coef_)

plt.figure(figsize=(10, 6))
plt.plot(alphas, coefs_lasso)
plt.xscale('log')
plt.xlabel('alpha')
plt.ylabel('კოეფიციენტები')
plt.title('სასჯელის პარამეტრის გავლენა Lasso რეგრესიის კოეფიციენტებზე')
plt.show()