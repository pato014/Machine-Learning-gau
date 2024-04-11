import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# Step 1: Read the CSV File
data = pd.read_csv("train_data.csv")

# Step 2: Prepare Features and Target Variable
X = data.drop('Price', axis=1)
y = data['Price']

# Step 3: Handle Missing Values in Target Variable
median_price = y.median()
y.fillna(median_price, inplace=True)

# Step 4: Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Define Preprocessing Pipeline
categorical_features = ['Manufacturer', 'Model', 'Category', 'Fuel type', 'Engine Volume', 'Gear box type', 'Year']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
numerical_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Step 6: Create Pipeline with Preprocessing and Model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', Ridge(alpha=1.0))  # Add regularization with Ridge regression
])

# Step 7: Train the Model
model.fit(X_train, y_train)

# Step 8: Make Predictions
y_pred = model.predict(X_test)

# Step 9: Evaluate the Model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Step 10: Predict Prices for New Data
new_data = pd.read_csv("full_cars_data.csv")  # Load new data
predicted_prices = model.predict(new_data)  # Predict prices for new data
print("Predicted Prices for New Data:")
for index, price in enumerate(predicted_prices):
    manufacturer = new_data.iloc[index]['Manufacturer']
    model_name = new_data.iloc[index]['Model']
    year = new_data.iloc[index]['Year']
    print("Manufacturer: {}, Model: {}, Year: {}, Predicted Price: ${:.2f}".format(manufacturer, model_name, year, price))

predicted_data = pd.DataFrame({
    'Manufacturer': new_data['Manufacturer'],
    'Model': new_data['Model'],
    "Year": new_data['Year'],
    'Predicted Price': predicted_prices
})

# Save Predicted Prices to CSV
predicted_data.to_csv("predicted_prices.csv", index=False)
print("Predicted prices saved to predicted_prices.csv file.")