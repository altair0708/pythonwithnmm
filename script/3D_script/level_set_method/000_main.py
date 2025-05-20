import numpy as np
import matplotlib.pyplot as plt

# 设置矩形板参数
W, H = 1.0, 2.0
nx, ny = 50, 100
dx, dy = W/nx, H/ny

# 生成网格点
x = np.linspace(0, W, nx+1)
y = np.linspace(0, H, ny+1)
X, Y = np.meshgrid(x, y)

# 初始裂纹信息
crack_tip = [0.2, H/2]
crack_angle = 0  # 初始水平裂纹

# 水平集函数
def compute_level_sets(X, Y, crack_tip, angle):
    """
    计算φ(x), ψ(x) 两个水平集函数
    φ: 裂缝距离函数
    ψ: 沿裂缝方向的距离函数
    """
    x0, y0 = crack_tip
    n = np.array([np.cos(angle), np.sin(angle)])
    t = np.array([-n[1], n[0]])  # 法向量

    Xv = X - x0
    Yv = Y - y0

    phi = Xv * t[0] + Yv * t[1]
    psi = Xv * n[0] + Yv * n[1]
    return phi, psi

# 可视化水平集
def plot_level_sets(phi, psi, X, Y, crack_tip, title):
    plt.figure(figsize=(6, 10))
    plt.contour(X, Y, phi, levels=[0], colors='r', linewidths=2, linestyles='--')
    plt.contour(X, Y, psi, levels=[0], colors='b', linewidths=2)
    plt.plot(crack_tip[0], crack_tip[1], 'ko', label='Crack Tip')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.show()

# 模拟裂纹扩展
def propagate_crack(crack_tip, angle, da):
    """沿 angle 方向扩展 da 距离"""
    x_new = crack_tip[0] + da * np.cos(angle)
    y_new = crack_tip[1] + da * np.sin(angle)
    return [x_new, y_new]

# 主程序
if __name__ == "__main__":
    steps = 5
    da = 0.05
    crack_path = [crack_tip]

    for i in range(steps):
        phi, psi = compute_level_sets(X, Y, crack_tip, crack_angle)
        plot_level_sets(phi, psi, X, Y, crack_tip, f"Level Set @ Step {i+1}")

        # 使用最大环向应力准则（这里只做演示，保持水平）
        new_tip = propagate_crack(crack_tip, crack_angle, da)
        crack_path.append(new_tip)
        crack_tip = new_tip  # 更新裂尖

    # 绘制裂纹路径
    crack_path = np.array(crack_path)
    plt.plot(crack_path[:, 0], crack_path[:, 1], 'k-o')
    plt.title("Crack Propagation Path")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.axis('equal')
    plt.show()
