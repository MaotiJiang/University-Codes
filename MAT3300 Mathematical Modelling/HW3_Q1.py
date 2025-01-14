import numpy as np
import matplotlib.pyplot as plt

# Initial conditions for bass and trout populations
B_0 = 5  # Initial population of bass
T_0 = 2  # Initial population of trout

# Time parameters
dt = 0.01  # Time step size
total_time = 2  # Total time for simulation

# Case 1: α = β = 0 (No intra-species competition)
alpha_1 = 0
beta_1 = 0

# Case 2: α = 1 and β = 2 (With intra-species competition)
alpha_2 = 1
beta_2 = 2

# Euler's method function for both cases
def euler_method(alpha, beta, B_0, T_0, dt, total_time):
    # Variables to store populations over time
    B = B_0
    T = T_0

    # Lists to store results for plotting
    t_list = []  # To store time values
    B_list = []  # To store bass population over time
    T_list = []  # To store trout population over time

    t = 0  # Reset time to 0 for the simulation
    while t <= total_time:
        # Store the current values of time and populations
        t_list.append(t)
        B_list.append(B)
        T_list.append(T)

        # Compute derivatives using the given differential equations
        dB = B * (10 - B - T) - alpha * B**2
        dT = T * (15 - B - 3 * T) - beta * T**2

        # Update populations using Euler's method
        B = B + dB * dt
        T = T + dT * dt

        # Increment time
        t += dt

    return t_list, B_list, T_list

# Run Euler's method for both cases
t_list_1, B_list_1, T_list_1 = euler_method(alpha_1, beta_1, B_0, T_0, dt, total_time)
t_list_2, B_list_2, T_list_2 = euler_method(alpha_2, beta_2, B_0, T_0, dt, total_time)

# Plot results for Case 1: α = β = 0
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(t_list_1, B_list_1, label="Bass Population (B)", color='blue')
plt.plot(t_list_1, T_list_1, label="Trout Population (T)", color='green')
plt.xlabel("Time (t)")
plt.ylabel("Population")
plt.title("Case 1: α = 0, β = 0 (No within Species Competition)")
plt.legend()
plt.grid()

# Plot results for Case 2: α = 1, β = 2
plt.subplot(1, 2, 2)
plt.plot(t_list_2, B_list_2, label="Bass Population (B)", color='blue')
plt.plot(t_list_2, T_list_2, label="Trout Population (T)", color='green')
plt.xlabel("Time (t)")
plt.ylabel("Population")
plt.title("Case 2: α = 1, β = 2 (Within Species Competition)")
plt.legend()
plt.grid()

# Show the figures
plt.tight_layout()
plt.show()
