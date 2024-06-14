import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/Users/luoyaxin/Desktop/DB4_Group1/filtered_data.csv')

# Assuming the first row could be headers, let's ensure to remove any non-numeric rows. 
# Convert columns to numeric, coercing errors to NaN (not a number)
data['temperature'] = pd.to_numeric(data['temperature'], errors='coerce')
data['pump cooler freq'] = pd.to_numeric(data['pump cooler freq'], errors='coerce')
data['concentration'] = pd.to_numeric(data['concentration'], errors='coerce')
data['light intensity'] = pd.to_numeric(data['light intensity'], errors='coerce')

# Check and drop any rows that contain NaN values (which might have been caused by conversion issues)
data.dropna(inplace=True)

# Now let's scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(data_scaled)

# Add cluster information back to the dataframe
data['Cluster'] = clusters

# Plotting clusters
plt.scatter(data['temperature'], data['light intensity'], c=data['Cluster'], cmap='viridis')
plt.xlabel('Temperature')
plt.ylabel('Light Intensity')
plt.title('Data Clusters by Temperature and Light Intensity')
plt.colorbar()
plt.show()
# # Split the data into features and target variable
# # Assuming 'algae growth rate' is a column in your dataset, replace 'algae_growth_rate' with the correct column name
# X = data.drop('algae_growth_rate', axis=1)
# y = data['algae_growth_rate']   

# # Split data into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Scale the features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# # Initialize the model
# model = LinearRegression()

# # Train the model
# model.fit(X_train_scaled, y_train)
# # Make predictions
# y_pred = model.predict(X_test_scaled)

# # Evaluate the predictions
# mse = mean_squared_error(y_test, y_pred)
# print(f'Mean Squared Error: {mse}')
# # Example of making a prediction
# # You need to provide an array with values for temperature, pump cooler freq, concentration, light intensity
# new_data = np.array([[31, 16025, -410175, 4095]])  # Example new data
# new_data_scaled = scaler.transform(new_data)
# predicted_growth_rate = model.predict(new_data_scaled)
# print(f'Predicted Algae Growth Rate: {predicted_growth_rate[0]}')
