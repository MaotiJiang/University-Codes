import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
x_0 = 0.5  # Initial prey population
y_0 = 1    # Initial predator population

# Time parameters
dt = 0.01  # Time step size
total_time = 1  # Total time for simulation

# Define Euler's method function for the two cases
def euler_method(x_0, y_0, alpha, beta, dt, total_time):
    # Initialize variables
    x = x_0
    y = y_0

    # Lists to store results
    t_list = [0]
    x_list = [x_0]
    y_list = [y_0]

    t = 0  # Start time
    while t <= total_time:
        # Calculate the derivatives based on the differential equations
        dx = x - x * y - 3/4 * x - alpha * x**2
        dy = x * y - y - 3/4 * y - beta * y**2

        # Update populations using Euler's method
        x = x + dx * dt
        y = y + dy * dt

        # Increment time
        t += dt

        # Store the new values
        t_list.append(t)
        x_list.append(x)
        y_list.append(y)

    return t_list, x_list, y_list

# Run Euler's method for the three cases
# 1. Original model (no internal competition): alpha = 0, beta = 0
t_orig, x_orig, y_orig = euler_method(x_0, y_0, alpha=0, beta=0, dt=dt, total_time=total_time)

# 2. Internal competition for prey: alpha = 0.5, beta = 0.2
t_comp_prey, x_comp_prey, y_comp_prey = euler_method(x_0, y_0, alpha=0.5, beta=0.2, dt=dt, total_time=total_time)

# 3. Internal competition for both: alpha = 0.5, beta = 0.5
t_comp_both, x_comp_both, y_comp_both = euler_method(x_0, y_0, alpha=0.5, beta=0.5, dt=dt, total_time=total_time)

# 4. Internal competition for both: alpha = 0.2, beta = 0.5
t_comp_tor, x_comp_tor, y_comp_tor = euler_method(x_0, y_0, alpha=0.2, beta=0.5, dt=dt, total_time=total_time)

# Plot the trajectories
plt.figure(figsize=(12, 6))

# Plot for the original model
plt.plot(t_orig, x_orig, label='Prey (Original)', linestyle='-', color='blue',linewidth=2)
plt.plot(t_orig, y_orig, label='Predator (Original)', linestyle='-', color='blue',linewidth=2)

# Plot for intra-species competition for prey
plt.plot(t_comp_prey, x_comp_prey, label='Prey (Comp for Prey Only alpha=0.5, beta=0.2)', linestyle='--', color='red')
plt.plot(t_comp_prey, y_comp_prey, label='Predator (Comp for Prey Only alpha=0.5, beta=0.2)', linestyle='--', color='red')

# Plot for intra-species competition for both species
plt.plot(t_comp_both, x_comp_both, label='Prey (Comp for Both alpha=0.5, beta=0.5)', linestyle='-.', color='yellow')
plt.plot(t_comp_both, y_comp_both, label='Predator (Comp for Both alpha=0.5, beta=0.5)', linestyle='-.', color='yellow')

# Plot for intra-species competition for both species
plt.plot(t_comp_tor, x_comp_tor, label='Prey (Comp for tor alpha=0.2, beta=0.5)', linestyle=':', color='green',linewidth=2)
plt.plot(t_comp_tor, y_comp_tor, label='Predator (Comp for tor alpha=0.2, beta=0.5)', linestyle=':', color='green',linewidth=2)

# Labels and legend
plt.xlabel('Time (t)')
plt.ylabel('Population')
plt.title('Population Dynamics for Predator-Prey Model with Harvesting and Internal Competition')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

plt.plot(x_orig, y_orig,label='Original', linestyle='-', color='blue')
plt.plot(x_comp_prey, y_comp_prey,label='Competition alpha=0.5, beta=0.2 ', linestyle='-', color='red')
plt.plot(x_comp_both, y_comp_both,label='Competition alpha=0.5, beta=0.5 ', linestyle='-', color='yellow')
plt.plot(x_comp_tor, y_comp_tor,label='Competition alpha=0.2, beta=0.5 ', linestyle='-', color='green')

# Labels and legend
plt.xlabel('Prey Population(x)')
plt.ylabel('Predator Population(y)')
plt.title('Population Dynamics for Predator-Prey Model between species')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()