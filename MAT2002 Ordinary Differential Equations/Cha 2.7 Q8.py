import numpy as np
import matplotlib.pyplot as plt

# Define the differential equation
def dydt(t, y):
    return   -t*y+0.1*y**3

# Generate a grid of t and y values
t_values = np.linspace(-10, 10, 20)  # t from -10 to 10
y_values = np.linspace(-8, 8, 20)  # y from -8 to 8

# Create a meshgrid for the t and y values
T, Y = np.meshgrid(t_values, y_values)

# Calculate the slopes at each grid point
DYDT = dydt(T, Y)

# Normalize the slopes for uniform arrow sizes
m = np.sqrt(1 + DYDT**2)
U = 1 / m  # Change in t is always 1, so it's normalized to 1 / m
V = DYDT / m  # Change in y is DYDT, so it's normalized to DYDT / m

# Plot the direction field
plt.figure(figsize=(10, 6))
plt.quiver(T, Y, U, V, angles="xy")
plt.xlim([-5, 10])
plt.ylim([-8, 8])
plt.xlabel('t')
plt.ylabel('y')
plt.title("Direction Field for y' = -ty + 0.1y^3")
plt.grid(True)
plt.show()