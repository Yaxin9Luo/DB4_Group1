import numpy as np
import matplotlib.pyplot as plt

# Filtration rate parameters
a = 3.27
b = 38.2
F_max = 100
K = 5000

# Temperature and food concentration ranges
T = np.linspace(8.3, 20, 100)
C = np.linspace(0, 20000, 100)

# Meshgrid for 3D plot
T_grid, C_grid = np.meshgrid(T, C)
F_T = a * T_grid + b
F_C = (F_max * C_grid) / (K + C_grid)
F_combined = F_T * F_C / F_max

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(T_grid, C_grid, F_combined, cmap='viridis')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Food Concentration (cells mL^-1)')
ax.set_zlabel('Filtration Rate (mL min^-1 ind^-1)')
ax.set_title('Mussel Filtration Rate vs. Temperature and Food Concentration')
plt.show()
