import matplotlib.pyplot as plt
import numpy as np

# Data
concentration = np.array([600, 800, 1200, 2400, 3000, 6000, 10000, 20000])
clearance_rates = np.array([0.030973, 0.726, 0.85, 1.9, 1.8332, 2.69, 2.45, 1.12])
sd = np.array([0.002603, 0.154, 0.038, 3.37, 0.2726, 0.44, 0.22, 0.5])
weights = np.ones_like(concentration)
weights[3] = 1

# Polynomial fit
degree = 3  # Polynomial degree
coef = np.polyfit(np.log(concentration), clearance_rates, degree, w=weights)
poly_func = np.poly1d(coef)

# Generating points for the polynomial line on the actual concentration range
x_poly = np.linspace(min(concentration), max(concentration), 400)
y_poly = poly_func(np.log(x_poly))  # Apply polynomial function after logarithmic transformation of x

# Plotting
plt.figure(figsize=(10, 6))
plt.errorbar(concentration, clearance_rates, yerr=sd, fmt='o', capsize=5, capthick=2, ecolor='red', marker='o', linestyle='None', markersize=8, color='blue', label='Data with error')
plt.plot(x_poly, y_poly, 'b-', label=f'{degree} Degree Polynomial Fit')
plt.title('Concentration vs Clearance Rates')
plt.xlabel('Concentration (L/h per mussel)')
plt.ylabel('Clearance Rates (L/h)')
plt.grid(True)
plt.legend()
plt.show()

# Function to predict clearance rates
def predict_clearance(conc):
    return poly_func(np.log(conc))

# Example: Predict clearance rate for new concentrations
new_concentrations = [1500, 5000, 15000]
predictions = [predict_clearance(c) for c in new_concentrations]
print("Predicted clearance rates:")
for conc, pred in zip(new_concentrations, predictions):
    print(f"Concentration: {conc} L/h -> Clearance Rate: {pred:.4f} L/h")

######################### Naive Polynomial Fit #########################

######################### None Linear Regression #########################
# from scipy.optimize import curve_fit

# # Define the Michaelis-Menten function
# def michaelis_menten(conc, Vmax, Km):
#     return (Vmax * conc) / (Km + conc)

# # Fit the model
# params, cov = curve_fit(michaelis_menten, concentration, clearance_rates)
# Vmax, Km = params

# # Plotting the fit
# plt.figure(figsize=(10, 6))
# plt.scatter(concentration, clearance_rates, color='red', label='Data Points')
# x_vals = np.linspace(min(concentration), max(concentration), 200)
# y_vals = michaelis_menten(x_vals, Vmax, Km)
# plt.plot(x_vals, y_vals, label='Michaelis-Menten Fit: Vmax=%.2f, Km=%.2f' % (Vmax, Km))
# plt.xlabel('Concentration')
# plt.ylabel('Clearance Rates (L/h)')
# plt.title('Nonlinear Regression: Michaelis-Menten Kinetics')
# plt.legend()
# plt.xscale('log')
# plt.grid(True)
# plt.show()
######################### None Linear Regression #########################

######################### Random Forest #########################
# from sklearn.ensemble import RandomForestRegressor

# # Fit the model
# rf = RandomForestRegressor(n_estimators=100, random_state=42)
# rf.fit(concentration, clearance_rates)

# # Plotting predictions
# x_plot = np.linspace(min(concentration), max(concentration), 400).reshape(-1, 1)
# y_plot = rf.predict(x_plot)

# plt.figure(figsize=(10, 6))
# plt.scatter(concentration, clearance_rates, color='blue', label='Data Points')
# plt.plot(x_plot, y_plot, color='green', label='Random Forest Prediction')
# plt.xlabel('Concentration')
# plt.ylabel('Clearance Rates (L/h)')
# plt.title('Machine Learning: Random Forest')
# plt.legend()
# plt.xscale('log')
# plt.grid(True)
# plt.show()
######################### Random Forest #########################