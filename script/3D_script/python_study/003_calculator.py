import numpy as np
import pandas as pd

# 参数
g = 9.8  # m/s^2
dt = 0.02
t = np.arange(0, 1.0 + dt, dt)  # 从0到1s，间隔0.02s

# 位移公式 s = 0.5 * g * t^2
s = 0.5 * g * t**2

# 制作表格
df = pd.DataFrame({
    "time (s)": np.round(t, 2),
    "displacement (m)": np.round(s, 4)
})
