import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
Q1_0 = 25  # Initial amount of salt in Tank 1 (oz)
Q2_0 = 15  # Initial amount of salt in Tank 2 (oz)

# Time parameters
dt = 0.1  # Time step size
total_time = 100  # Total time for simulation
t = 0  # Starting time

# Variables to store salt quantities over time
Q1 = Q1_0
Q2 = Q2_0

# Lists to store results for plotting
t_list = []  # To store time values
Q1_list = []  # To store salt amount in Tank 1 over time
Q2_list = []  # To store salt amount in Tank 2 over time

# Euler's method to update the values over time
while t < total_time:
    # Store the current values of time and salt concentrations
    t_list.append(t)
    Q1_list.append(Q1)
    Q2_list.append(Q2)

    # Compute derivatives using the differential equations
    dQ1 = 1.5 + 0.075 * Q2 - 0.1 * Q1
    dQ2 = 0.1 * Q1 + 3 - 0.2 * Q2

    # Update quantities using Euler's method
    Q1 = Q1 + dQ1 * dt
    Q2 = Q2 + dQ2 * dt

    # Increment time
    t += dt

# Plot the results for Q1(t) and Q2(t)
plt.figure(figsize=(10, 6))
plt.plot(t_list, Q1_list, label="Q1(t) - Salt in Tank 1 (oz)", marker='o')
plt.plot(t_list, Q2_list, label="Q2(t) - Salt in Tank 2 (oz)", marker='x')
plt.xlabel("Time (minutes)")
plt.ylabel("Amount of Salt (oz)")
plt.title("Salt Concentration vs. Time for Tank 1 and Tank 2")
plt.legend()
plt.grid()
plt.show()
