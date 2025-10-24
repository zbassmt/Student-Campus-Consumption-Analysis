import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 读取CSV文件并显示前几行和列名
file_path = r'C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\学生校园消费行为分析\task1_2_1.csv'

# 尝试使用utf-8编码读取文件
try:
    df = pd.read_csv(file_path, sep=',', encoding='utf-8')
except UnicodeDecodeError:
    print("使用utf-8编码读取文件失败，尝试使用gbk编码")
    df = pd.read_csv(file_path, sep=',', encoding='gbk', encoding_errors='replace')

# 显示前几行数据
print(df.head())

# 计算人均刷卡频次(总刷卡次数/学生总人数)
cost_count = df['Date'].count()
student_count = df['CardNo'].nunique()  # 使用nunique()而不是value_counts().count()以避免NaN问题
average_cost_count = int(round(cost_count / student_count))
print("人均刷卡频次:", average_cost_count)

# 计算人均消费额(总消费金额/学生总人数)
cost_sum = df['Money'].sum()
average_cost_money = int(round(cost_sum / student_count))
print("人均消费额:", average_cost_money)

# 设置字体
font_path = r"C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\OPPOSans-R.ttf"
try:
    font = FontProperties(fname=font_path)
except Exception as e:
    print(f"加载字体失败: {e}")
    font = None

# 设置全局字体配置
plt.rcParams['font.sans-serif'] = ['OPPOSans'] if font is None else [font.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置中文字体
font = FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

# 提高分辨率
plt.rcParams['figure.dpi'] = 150


# 计算不同专业、不同性别人均消费
data_gb1 = df['Money'].groupby(df['Major']).mean().reset_index()
data_gb2 = df['Money'].groupby([df['Sex'], df['Major']]).mean().reset_index()
data_boy = data_gb2[data_gb2['Sex'] == '男']
data_girl = data_gb2[data_gb2['Sex'] == '女']

# 分别选取了18国际金融、18计算机应用、18建筑工程三个专业。
major = ['18国际金融','18计算机应用','18建筑工程']
data_gb3 = data_gb1.loc[data_gb1['Major'].isin(major)]
data_boy1 = data_boy.loc[data_boy['Major'].isin(major)]
data_girl1 = data_girl.loc[data_girl['Major'].isin(major)]
# 绘制三个专业、不同性别人均消费柱状图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
p = plt.figure(figsize = (12,6))  # 将画布设定为正方形，则绘制的饼图是正圆
ax1 = p.add_subplot(1,3,1)
plt.bar(data_gb3['Major'], data_gb3['Money'])
plt.title('不同专业人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
ax2 = p.add_subplot(1,3,2)
plt.bar(data_boy1['Major'], data_boy1['Money'])
plt.title('男生人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
ax3 = p.add_subplot(1,3,3)
plt.bar(data_girl1['Major'], data_girl1['Money'])
plt.title('女生人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
plt.show()


#######################################################################################################################
# 计算每个学生的总消费金额
student_total_cost = df.groupby('CardNo')['Money'].sum()

# 计算每个学生的平均消费金额
student_average_cost = student_total_cost / df.groupby('CardNo')['Date'].count()

# 打印前几行的平均消费金额
print(student_average_cost.head())

# 打印平均消费金额的描述性统计信息
print(student_average_cost.describe())

# 定义人均消费额的界限
threshold = student_average_cost.median()  # 使用中位数作为阈值

# 打印阈值
print("调整后的阈值:", threshold)

# 划分两个群体
high_spending = df[df['CardNo'].isin(student_average_cost[student_average_cost > threshold].index)]
low_spending = df[df['CardNo'].isin(student_average_cost[student_average_cost <= threshold].index)]

# 打印高消费群体和低消费群体的样本数量
print("高消费群体样本数量:", len(high_spending['CardNo'].unique()))
print("低消费群体样本数量:", len(low_spending['CardNo'].unique()))

# 打印高消费群体和低消费群体的平均消费金额
print("高消费群体平均消费金额:")
print(student_average_cost[student_average_cost > threshold].describe())

print("低消费群体平均消费金额:")
print(student_average_cost[student_average_cost <= threshold].describe())

# 统计高消费群体在不同消费地点的消费次数
high_spending_counts = high_spending['Dept'].value_counts()

# 统计低消费群体在不同消费地点的消费次数
low_spending_counts = low_spending['Dept'].value_counts()

# 检查数据是否为空
if high_spending_counts.empty:
    print("高消费群体数据为空")
else:
    print("高消费群体消费地点分布:")
    print(high_spending_counts)

if low_spending_counts.empty:
    print("低消费群体数据为空")
else:
    print("低消费群体消费地点分布:")
    print(low_spending_counts)

# 设置字体
font_path = r"C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\OPPOSans-R.ttf"
try:
    font = FontProperties(fname=font_path)
except Exception as e:
    print(f"加载字体失败: {e}")
    font = None

# 设置全局字体配置
plt.rcParams['font.sans-serif'] = ['OPPOSans'] if font is None else [font.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置中文字体
font = FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

# 提高分辨率
plt.rcParams['figure.dpi'] = 150

# 创建画布
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# 绘制高消费群体的消费地点分布（饼图）
if not high_spending_counts.empty:
    high_spending_counts.plot(kind='pie', ax=axes[0], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightblue', 'lightgreen', 'lightcoral', 'lightsalmon'])
    axes[0].set_title("高消费群体消费地点分布", fontproperties=font, fontsize=20)
    axes[0].set_ylabel("")  # 去掉默认的y轴标签
else:
    axes[0].text(0.5, 0.5, "高消费群体数据为空", fontsize=20, ha='center', va='center')

# 绘制低消费群体的消费地点分布（饼图）
if not low_spending_counts.empty:
    low_spending_counts.plot(kind='pie', ax=axes[1], autopct='%1.1f%%', startangle=90, colors=['salmon', 'lightcoral', 'lightsalmon', 'lightpink', 'lightgrey'])
    axes[1].set_title("低消费群体消费地点分布", fontproperties=font, fontsize=20)
    axes[1].set_ylabel("")  # 去掉默认的y轴标签
else:
    axes[1].text(0.5, 0.5, "低消费群体数据为空", fontsize=20, ha='center', va='center')

# 显示图像
plt.tight_layout()
plt.show()

# 打印低消费群体的平均消费金额描述性统计信息
print("低消费群体平均消费金额:")
print(student_average_cost[student_average_cost <= threshold].describe())

# 统计低消费群体在不同消费地点的消费次数
low_spending_counts = low_spending['Dept'].value_counts()

if not low_spending_counts.empty:
    print("低消费群体消费地点分布:")
    print(low_spending_counts)
else:
    print("低消费群体数据为空")

# 绘制低消费群体的消费地点分布（饼图）
fig, ax = plt.subplots(figsize=(8, 6))
if not low_spending_counts.empty:
    low_spending_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=['salmon', 'lightcoral', 'lightsalmon', 'lightpink', 'lightgrey'])
    ax.set_title("低消费群体消费地点分布", fontproperties=font, fontsize=20)
    ax.set_ylabel("")  # 去掉默认的y轴标签
else:
    ax.text(0.5, 0.5, "低消费群体数据为空", fontsize=20, ha='center', va='center')

plt.tight_layout()
plt.show()

df['hour'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M')
# 分析低消费群体的消费时间段分布
low_spending_hourly = low_spending.groupby('hour')['Money'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='hour', y='Money', data=low_spending_hourly)
plt.title('低消费群体按小时消费金额分布', fontsize=20)
plt.xlabel('小时', fontsize=14)
plt.ylabel('消费金额', fontsize=14)
plt.xticks(rotation=90)
plt.show()

# 分析低消费群体的月就餐次数
low_spending_monthly = low_spending.groupby('CardNo')['Date'].count().reset_index()
low_spending_monthly.columns = ['CardNo', '月就餐次数']

plt.figure(figsize=(10, 6))
sns.histplot(data=low_spending_monthly, x='月就餐次数', bins=20, kde=True)
plt.title('低消费群体月就餐次数分布', fontsize=20)
plt.xlabel('月就餐次数', fontsize=14)
plt.ylabel('人数', fontsize=14)
plt.show()

# 分析低消费群体的性别和专业差异
low_spending_gender_major = low_spending.groupby(['Sex', 'Major'])['Money'].mean().reset_index()

plt.figure(figsize=(12, 8))
sns.barplot(data=low_spending_gender_major, x='Major', y='Money', hue='Sex')
plt.title('低消费群体按性别和专业的人均消费额', fontsize=20)
plt.xlabel('专业', fontsize=14)
plt.ylabel('人均消费额', fontsize=14)
plt.xticks(rotation=90)
plt.show()


# 打印低消费群体的平均消费金额描述性统计信息
print("低消费群体平均消费金额:")
print(student_average_cost[student_average_cost <= threshold].describe())
import pandas as pd

# Assuming low_spending is your DataFrame
low_spending['Date'] = pd.to_datetime(low_spending['Date'])

# 分析低消费群体的消费时间段分布
low_spending['hour'] = low_spending['Date'].dt.hour
low_spending_hourly = low_spending.groupby('hour')['Money'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='hour', y='Money', data=low_spending_hourly)
plt.title('低消费群体按小时消费金额分布', fontsize=20)
plt.xlabel('小时', fontsize=14)
plt.ylabel('消费金额', fontsize=14)
plt.xticks(rotation=90)
plt.show()

# 分析低消费群体的月就餐次数
low_spending_monthly = low_spending.groupby('CardNo')['Date'].count().reset_index()
low_spending_monthly.columns = ['CardNo', '月就餐次数']

plt.figure(figsize=(10, 6))
sns.histplot(data=low_spending_monthly, x='月就餐次数', bins=20, kde=True)
plt.title('低消费群体月就餐次数分布', fontsize=20)
plt.xlabel('月就餐次数', fontsize=14)
plt.ylabel('人数', fontsize=14)
plt.show()

# 分析低消费群体的性别和专业差异
low_spending_gender_major = low_spending.groupby(['Sex', 'Major'])['Money'].mean().reset_index()

plt.figure(figsize=(12, 8))
sns.barplot(data=low_spending_gender_major, x='Major', y='Money', hue='Sex')
plt.title('低消费群体按性别和专业的人均消费额', fontsize=20)
plt.xlabel('专业', fontsize=14)
plt.ylabel('人均消费额', fontsize=14)
plt.xticks(rotation=90)
plt.show()
