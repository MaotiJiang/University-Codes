import numpy as np
import matplotlib.pyplot as plt

# parameters
T0 = 100              # Initial temperature
Ta = 20               # Ambient temperature
k = 0.1               # Cooling constant set as 0.1
dt = 0.1              # Time step


t = 0  # Initial temperature
T= T0
t_list=[]
T_list=[]
# Euler's method to update temperature

while t<100: #set total time as 100
    T += k*(Ta-T)*dt
    t+=dt
    t_list.append(t)
    T_list.append(T)


# Plotting the results
plt.plot(t_list, T_list, label="Euler's Method (Numerical)")

plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature of the Cake Over Time')
plt.legend()
plt.grid()
plt.show()
