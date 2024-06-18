import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Time points (hours)
time = np.array([0, 1, 2, 3, 4, 5, 24])

# Algae count data for three bottles
bottle1 = np.array([51083, 31532, 33750, 28898, 34792, 32243, 56695])
bottle2 = np.array([40711, 35605, 28599, 33804, 31126, 32283.5, 63550])
bottle3 = np.array([49674, 45409, 40693, 41797, 44733, 43158, 73636])

# Combine data for ease of processing
data = np.array([bottle1, bottle2, bottle3])

# Define the exponential growth model
def exponential_model(t, N0, r):
    return N0 * np.exp(r * t)

# Fit the model to each bottle's data
params1, _ = curve_fit(exponential_model, time, bottle1)
params2, _ = curve_fit(exponential_model, time, bottle2)
params3, _ = curve_fit(exponential_model, time, bottle3)

# Extract parameters
N0_1, r_1 = params1
N0_2, r_2 = params2
N0_3, r_3 = params3

# Generate time points for prediction
time_pred = np.linspace(0, 24, 100)

# Predict using the fitted model
pred1 = exponential_model(time_pred, N0_1, r_1)
pred2 = exponential_model(time_pred, N0_2, r_2)
pred3 = exponential_model(time_pred, N0_3, r_3)

# Plot the results
plt.figure(figsize=(12, 6))

# Plot bottle 1
plt.subplot(1, 3, 1)
plt.scatter(time, bottle1, label='Data')
plt.plot(time_pred, pred1, label='Fit', color='red')
plt.title('Bottle 1')
plt.xlabel('Time (hours)')
plt.ylabel('Algae Count')
plt.legend()

# Plot bottle 2
plt.subplot(1, 3, 2)
plt.scatter(time, bottle2, label='Data')
plt.plot(time_pred, pred2, label='Fit', color='red')
plt.title('Bottle 2')
plt.xlabel('Time (hours)')
plt.ylabel('Algae ')
plt.legend()

# Plot bottle 3
plt.subplot(1, 3, 3)
plt.scatter(time, bottle3, label='Data')
plt.plot(time_pred, pred3, label='Fit', color='red')
plt.title('Bottle 3')
plt.xlabel('Time (hours)')
plt.ylabel('Algae')
plt.legend()

plt.tight_layout()
plt.show()


################## growth rate calculation ##################
# Function to calculate growth rate
def calculate_growth_rate(data):
    growth_rate = np.diff(data) / data[:-1]
    return growth_rate

# Calculate growth rates for each bottle
growth_rate_bottle1 = calculate_growth_rate(bottle1)
growth_rate_bottle2 = calculate_growth_rate(bottle2)
growth_rate_bottle3 = calculate_growth_rate(bottle3)

# Print results
print("Growth rates for Bottle 1:", growth_rate_bottle1)
print("Growth rates for Bottle 2:", growth_rate_bottle2)
print("Growth rates for Bottle 3:", growth_rate_bottle3)

