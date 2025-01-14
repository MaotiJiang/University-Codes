import numpy as np
import matplotlib.pyplot as plt
# Define the Heaviside step function
def heaviside(t):
    return 0.5 * (np.sign(t) + 1)
# Define the function y(t)
def y(t):
    return ((-16/17) * np.cos(t) + (4/17) * np.sin(t) +(16/17) * np.exp(-t/2) * np.cos(t) +(4/17) * np.exp(-t/2) * np.sin(t) +((-16/17) * np.cos(t - np.pi) +(4/17) * np.sin(t - np.pi) +
             (16/17) * np.exp(-(t - np.pi)/2) * np.cos(t - np.pi) +
             (4/17) * np.exp(-(t - np.pi)/2) * np.sin(t - np.pi)) * heaviside(t - np.pi))
# Adjust the function g(t) to be defined for the range 0 to 2*pi, but zero outside 0 to pi
def g_adjusted(t):
    return np.sin(t) * (t >= 0) * (t < np.pi)
# Calculate g(t) for the same t values as y(t)
t_values = np.linspace(0, 4 * np.pi, 400)
g_adjusted_values = g_adjusted(t_values)
y_values = y(t_values)
# Plot y(t) and g(t) on the same graph
plt.figure(figsize=(10, 5))
plt.plot(t_values, y_values, label='y(t)')
plt.plot(t_values, g_adjusted_values, label='g(t) on [0, π]', linestyle='--')
plt.title('Plot of y(t) and g(t) on [0, 4π]')
plt.xlabel('t')
plt.ylabel('Function values')
plt.grid(True)
plt.legend()
plt.show()
