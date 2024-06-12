import numpy as np
import matplotlib.pyplot as plt

# Parameters
a = 3.27  # slope of the filtration rate vs. temperature relationship
b = 38.2  # intercept of the filtration rate vs. temperature relationship
T = np.linspace(8.3, 20, 100)  # temperature range (°C)

# Filtration rate as a function of temperature
F = a * T + b

plt.plot(T, F, label='Filtration Rate vs. Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Filtration Rate (mL min^-1 ind^-1)')
plt.legend()
plt.title('Mussel Filtration Rate vs. Temperature')
plt.show()

# Parameters for functional response
F_max = 100  # maximum filtration rate (mL min^-1 ind^-1)
K = 5000     # half-saturation constant (cells mL^-1)
C = np.linspace(0, 20000, 100)  # food concentration (cells mL^-1)

# Filtration rate as a function of food concentration
F_C = (F_max * C) / (K + C)

plt.plot(C, F_C, label='Filtration Rate vs. Food Concentration')
plt.xlabel('Food Concentration (cells mL^-1)')
plt.ylabel('Filtration Rate (mL min^-1 ind^-1)')
plt.legend()
plt.title('Mussel Filtration Rate vs. Food Concentration')
plt.show()
