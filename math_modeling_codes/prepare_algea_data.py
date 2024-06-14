import pandas as pd

# Load the data from the txt file
data = pd.read_csv('/Users/luoyaxin/Desktop/DB4_Group1/math_modeling_codes/Algae stats.txt', header=None)

# Define column names
data.columns = ['date and time', 'temperature', 'pump cooler freq', 'concentration', 'light intensity']

# Drop the 'date and time' column as we don't need it
data = data.drop(['date and time'], axis=1)

# Save the result to a new CSV file
data.to_csv('filtered_data.csv', index=False)

print("Data saved to 'filtered_data.csv'.")
