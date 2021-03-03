import pandas as pd  # 数据处理和分析，清洗
import matplotlib.pyplot as plt  # 数据可视化工具

# 引入数据
df = pd.read_csv('500.csv', header=None, index_col=0)
# 红球
# 所有行,1~6列
red_ball = df.loc[:, 1:5]
# print(red_ball)
# 篮球
blue_ball = df.loc[:, 6:7]
# print(blue_ball)

# 数据统计
# 记录每个号码出现的次数
red_ball_count = pd.value_counts(red_ball.values.flatten())
# print("red ball count:")
# print(red_ball_count)
# 数据单列，直接 pd.value_counts(blue_ball) 即可
blue_ball_count = pd.value_counts(blue_ball.values.flatten())
# print("-------------------------------------------\nblue ball count:")
# print(blue_ball_count)

# # 可视化（图标）
# fig, ax = plt.subplots(2, 1) # 一次创建多个图表，2行1列
# # 用饼图展示
# ax[0].pie(red_ball_count, labels = red_ball_count.index, radius = 1, wedgeprops = {'width' : 0.3})
# ax[0].pie(blue_ball_count, labels = blue_ball_count.index, radius = 0.5, wedgeprops = {'width' : 0.2})
# ax[1].plot(red_ball_count)
# ax[1].plot(blue_ball_count)

plt.pie(red_ball_count, labels=red_ball_count.index, radius=1, wedgeprops={'width': 0.3})
plt.pie(blue_ball_count, labels=blue_ball_count.index, radius=0.5, wedgeprops={'width': 0.2})
plt.show()
