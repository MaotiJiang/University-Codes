import numpy as np
import matplotlib.pyplot as plt

# Initial concentrations
A0 = 50
B0 = 30
C0 = 0

# Reaction rates
k1 = 0.1  # Rate for A -> B
k2 = 0.05  # Rate for B -> C
k3 = 0.02  # Rate for C -> A

# Time parameters
dt = 0.1  # Time step

# Set initial values
t = 0
A = A0
B = B0
C = C0
t_list = []  # To store time values
A_list = []  # To store concentration of A over time
B_list = []  # To store concentration of B over time
C_list = []  # To store concentration of C over time

# Euler's method to update concentrations over time
while t < 100:
    # Store the current values of time and concentrations
    t_list.append(t)
    A_list.append(A)
    B_list.append(B)
    C_list.append(C)

    # Update concentrations using Euler's method
    A = A + (-k1 * A + k3 * C) * dt
    B = B + (k1 * A - k2 * B) * dt
    C = C + (k2 * B - k3 * C) * dt

    # Update time
    t += dt

# Plot the concentrations over time
plt.figure(figsize=(10, 6))
plt.plot(t_list, A_list, label="[A](t)", marker='o')
plt.plot(t_list, B_list, label="[B](t)", marker='x')
plt.plot(t_list, C_list, label="[C](t)", marker='s')
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.title("Concentration vs. Time for Reaction A -> B -> C -> A")
plt.legend()
plt.grid()
plt.show()

