import numpy as np
from matplotlib import pyplot as plt
# plt.style.use("mm.mplstyle")
import math

#Q2(1)
t = 0
y0 = 0.5  # 确保y0定义
y = y0
t_list = []
y_list = []
dt = 0.01  # 确保定义了dt

while t < 18:
    y += (2 * math.cos(t) * y + math.cos(t)) * dt  # 使用math.cos函数
    t += dt
    t_list.append(t)
    y_list.append(y)
# 绘制图表并设置标签
plt.plot(t_list, y_list, label="Euler's Method")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.show()


#Q(2)2
t = 0
y0 = 0  # 确保y0定义
y = y0
t_list = []
y_list = []
dt = 0.01  # 确保定义了dt

while t < 18:
    y += (3 + 2 * math.cos(2 * t) - 0.25 * y) * dt  # 使用math.cos函数
    t += dt
    t_list.append(t)
    y_list.append(y)
# 绘制图表并设置标签
plt.plot(t_list, y_list, label="Euler's Method", color='red', linewidth=2, linestyle='--')
# 转换 t_list 为 NumPy 数组
t_factor = np.array(t_list)

# 使用 NumPy 的矢量化函数来处理数组操作
plt.plot(t_factor, 12 + 8/65 * np.cos(2 * t_factor) + 64/65 * np.sin(2 * t_factor) - 788/65 * np.exp(-0.25 * t_factor), label="Exact")

plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()