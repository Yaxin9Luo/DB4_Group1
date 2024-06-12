import numpy as np
import matplotlib.pyplot as plt

# Parameters
mu_max = 1.0  # maximum growth rate (day^-1)
alpha = 0.1   # initial slope of the curve (day^-1 * (μmol photons m^-2 s^-1)^-1)
E = np.linspace(0, 200, 100)  # irradiance (μmol photons m^-2 s^-1)

# Specific growth rate as a function of irradiance
mu = mu_max * np.tanh(alpha * E / mu_max)

# Initial cell density and time
N0 = 1e4  # initial cell density (cells mL^-1)
t = np.linspace(0, 10, 100)  # time (days)

# Growth over time for different irradiance levels
for E_val in [500]:
    mu_val = mu_max * np.tanh(alpha * E_val / mu_max)
    Nt = N0 * np.exp(mu_val * t)
    plt.plot(t, Nt, label=f'E = {E_val} μmol photons m^-2 s^-1')

plt.xlabel('Time (days)')
plt.ylabel('Cell Density (cells mL^-1)')
plt.legend()
plt.title('Algae Growth Over Time')
plt.show()
