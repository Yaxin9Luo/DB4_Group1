import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# Load the data from the CSV file
data = pd.read_csv('/Users/luoyaxin/Desktop/DB4_Group1/collected_previous_data.csv')

# Strip any leading or trailing whitespace characters from the column names
data.columns = data.columns.str.strip()

# Select the columns needed for the model
X = data[['temperature', 'light intensity']]  # features
y = data['concentration']                     # target

# Split the data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=0)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Visualization using matplotlib
plt.figure(figsize=(14, 6))
# Temperatures and Light Intensities for prediction lines
temperature_range = np.linspace(X_train['temperature'].min(), X_train['temperature'].max(), 100)
light_intensity_range = np.linspace(X_train['light intensity'].min(), X_train['light intensity'].max(), 100)
# Prepare data for prediction by using meshgrid
temperature_mesh, light_intensity_mesh = np.meshgrid(temperature_range, light_intensity_range)

# Flatten the meshgrid arrays and create a feature array
features = np.vstack([temperature_mesh.ravel(), light_intensity_mesh.ravel()]).T
predicted_concentration = model.predict(features).reshape(temperature_mesh.shape)

# Plot for temperature vs concentration
plt.subplot(1, 2, 1)
plt.scatter(X_train['temperature'], y_train, color='blue', label='Training data')
plt.scatter(X_test['temperature'], y_test, color='green', label='Test data')
plt.contourf(temperature_mesh, light_intensity_mesh, predicted_concentration, alpha=0.5, levels=100, cmap='viridis')
plt.colorbar(label='Predicted Concentration')
plt.title('Temperature vs Concentration')
plt.xlabel('Temperature')
plt.ylabel('Concentration')
plt.legend()

# Plot for light intensity vs concentration
plt.subplot(1, 2, 2)
plt.scatter(X_train['light intensity'], y_train, color='blue', label='Training data')
plt.scatter(X_test['light intensity'], y_test, color='green', label='Test data')
plt.contourf(temperature_mesh, light_intensity_mesh, predicted_concentration, alpha=0.5, levels=100, cmap='viridis')
plt.colorbar(label='Predicted Concentration')
plt.title('Light Intensity vs Concentration')
plt.xlabel('Light Intensity')
plt.ylabel('Concentration')
plt.legend()

plt.tight_layout()
plt.show()

################# prediction from trained model #################
# Predict future concentrations
# Define new data for prediction
new_data = np.array([
    [31.0, 1000],  # Example 1
    [32.5, 2000],  # Example 2
    [30.0, 6000]   # Example 3
])

# Make predictions for the new data
future_predictions = model.predict(new_data)

# Display predictions
for i, input_pair in enumerate(new_data):
    print(f"Predicted concentration for temperature {input_pair[0]} and light intensity {input_pair[1]}: {future_predictions[i]}")



features_mesh = np.vstack([temperature_mesh.ravel(), light_intensity_mesh.ravel()]).T
predicted_concentration_mesh = model.predict(features_mesh).reshape(temperature_mesh.shape)

# 3D Plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot for actual data points
ax.scatter(X['temperature'], X['light intensity'], y, color='b', label='Actual data')

# Surface plot for predicted concentration
ax.plot_surface(temperature_mesh, light_intensity_mesh, predicted_concentration_mesh, color='orange', alpha=0.5)

ax.set_xlabel('Temperature')
ax.set_ylabel('Light Intensity')
ax.set_zlabel('Concentration')
ax.legend()
ax.set_title('3D View of Linear Regression Fit')
plt.show()


############################ Decision Tree ############################
from sklearn.tree import DecisionTreeRegressor

# Fit a Decision Tree model
tree_model = DecisionTreeRegressor(max_depth=5)  # max_depth is a hyperparameter you can tune
tree_model.fit(X_train, y_train)

# Predict and evaluate
y_tree_pred = tree_model.predict(X_test)
tree_mse = mean_squared_error(y_test, y_tree_pred)
print(f'Mean Squared Error for Decision Tree: {tree_mse}')
# Make predictions for the new data
future_predictions = tree_model.predict(new_data)

# Display predictions
for i, input_pair in enumerate(new_data):
    print(f"Predicted concentration for temperature {input_pair[0]} and light intensity {input_pair[1]}: {future_predictions[i]}")