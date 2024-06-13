import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import random


file_path = 'interns.xlsx'

df_sheet1 = pd.read_excel(file_path, sheet_name='Sheet1')
df_sheet2 = pd.read_excel(file_path, sheet_name='Sheet2')

# საშუალოს გამოთვლა
hr_mean_scores = df_sheet1.iloc[:, 1:].mean(axis=1)
it_mean_scores = df_sheet2.iloc[:, 1:].mean(axis=1)

df = pd.DataFrame({
    'Intern Code': df_sheet1['Intern Code'],
    'HR საშუალო ქულა': hr_mean_scores,
    'IT საშუალო ქულა': it_mean_scores
})

df.dropna(inplace=True)

# წრფივი რეგრესიის მოდელის შექმნა ყველა სტაჟიორისთვის
X = df[['HR საშუალო ქულა']].values
y = df[['IT საშუალო ქულა']].values

reg_model = LinearRegression()
reg_model.fit(X, y)

# IT ქულების განსაზღვრა
y_pred = reg_model.predict(X)

# რეგრესიული ხაზის პლოტის შექმნა
plt.figure(figsize=(10, 6))
sns.scatterplot(x='HR საშუალო ქულა', y='IT საშუალო ქულა', data=df)
plt.plot(df['HR საშუალო ქულა'], y_pred, color='red')
plt.xlabel('HR საშუალო ქულა')
plt.ylabel('IT საშუალო ქულა')
plt.title('HR საშუალო ქულა vs IT საშუალო ქულა')
plt.show()

print('Coefficient:', reg_model.coef_[0][0])
print('Intercept:', reg_model.intercept_[0])
print('R-squared:', reg_model.score(X, y))

# შემთხვევითად სტაჟიორის არჩევა
random_intern = random.choice(df['Intern Code'].unique())
print(f'Random Intern Code: {random_intern}')

# სტაჟიორის ქულების შეგროვება
hr_scores_random = df_sheet1[df_sheet1['Intern Code'] == random_intern].iloc[:, 1:].values.flatten()
it_scores_random = df_sheet2[df_sheet2['Intern Code'] == random_intern].iloc[:, 1:].values.flatten()

mask = ~np.isnan(hr_scores_random) & ~np.isnan(it_scores_random)
X_random = hr_scores_random[mask].reshape(-1, 1)
y_random = it_scores_random[mask].reshape(-1, 1)

# წრფივი რეგრესიის მოდელის შექმნა სტაჟიორისთვის
reg_model_random = LinearRegression()
reg_model_random.fit(X_random, y_random)

# IT ქულების განსაზღვრა
y_pred_random = reg_model_random.predict(X_random)

# რეგრესიის ხაზის პლოტირება
plt.figure(figsize=(10, 6))
plt.scatter(X_random, y_random, color='blue')
plt.plot(X_random, y_pred_random, color='red')
plt.xlabel('HR Score')
plt.ylabel('IT Score')
plt.title(f'HR ქულა vs IT ქულა სტაჟიორი {random_intern}-ისთვის')
plt.show()

print('Coefficient:', reg_model_random.coef_[0][0])
print('Intercept:', reg_model_random.intercept_[0])
print('R-squared:', reg_model_random.score(X_random, y_random))
