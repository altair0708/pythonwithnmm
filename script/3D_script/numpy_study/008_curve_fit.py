import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = np.array(
    [124997.5616, 106299.9572, 55993.59348, 57430.49631, 52128.23522, 17997.0525, 12233.42312, 3773.772147, 1864.771133,
     1206.99562, 275.3237799])
xdata = np.array([math.log10(x) for x in xdata])
ydata = np.array([2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5])


def func(x, a, b, c):
    ws = 31
    wr = 0
    return (ws - wr) / ((1 - (x / a) ** b) ** c) - wr


result, pcov = curve_fit(func, xdata, ydata, p0=[19, 4, 42], maxfev=5000)
print(result)

x_fit = np.linspace(xdata[0], xdata[-1], 100)
y_fit = func(x_fit, *result)

plt.scatter(xdata, ydata, label='Data')
plt.plot(x_fit, y_fit, 'r', label='Best fit curve')
plt.legend()
plt.show()

# import numpy as np
# from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt
#
# # 定义用于拟合的函数：正弦函数
# def func(x, amplitude, frequency, phase):
#     return amplitude * np.sin(2 * np.pi * frequency * x + phase)
#
# # 准备数据
# x = np.linspace(0, 2*np.pi, 100)  # 生成自变量 x
# y = 3 * np.sin(2 * np.pi * 2 * x + 0.5) # + np.random.normal(0, 0.2, 100)  # 生成带噪声的因变量 y
#
# # 调用 curve_fit 进行拟合
# popt, pcov = curve_fit(func, x, y, p0=(3, 2.1, 0.5))
#
# # 使用最佳拟合参数进行预测
# y_fit = func(x, *popt)
#
# # 打印最佳拟合参数
# print("Best fit parameters:", popt)
#
# # 绘制原始数据和拟合曲线
# plt.scatter(x, y, label='Data')
# plt.plot(x, y_fit, 'r', label='Best fit curve')
# plt.legend()
# plt.show()

