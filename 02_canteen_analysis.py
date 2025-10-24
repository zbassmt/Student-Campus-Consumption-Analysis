import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib.font_manager import FontProperties

# 读取CSV文件并显示前几行和列名
file_path = r'C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\学生校园消费行为分析\data2.csv'
df = pd.read_csv(file_path, sep=',', encoding='gbk')

# 显示前几行数据
print(df.head())

# 显示列名
print(df.columns)

# 将 Date 列转换为 datetime 类型
df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M')

# 判断是否为工作日
df['是否工作日'] = df['Date'].dt.weekday < 5  # 0-4为工作日，5-6为周末

# 打印结果
print(df)

# 显示数据类型
print(df.dtypes)

# 检查并过滤掉无效的日期值
invalid_dates = df[df['Date'].isna()]
print("无效日期的数量:", invalid_dates.shape[0])
print("无效日期的具体值:")
print(invalid_dates['Date'].head())

# 查看无效日期的具体值
print("无效日期的详细信息:")
print(invalid_dates.head(10))

# 过滤掉无效的日期值
df = df.dropna(subset=['Date'])

# 再次检查数据类型，确保Date列已经转换为datetime类型
if df['Date'].dtype == 'datetime64[ns]':
    print("Date列已经成功转换为datetime类型")
else:
    print("Date列转换失败，仍然为object类型")

# 添加时间段列
def get_time_period(hour):
    if 6 <= hour < 10:
        return '早'
    elif 10 <= hour < 17:
        return '中'
    else:
        return '晚'

df['时间段'] = df['Date'].dt.hour.apply(get_time_period)

# 过滤只包含 canteen1 到 canteen5 的记录
canteens = ['第一食堂', '第二食堂', '第三食堂', '第四食堂', '第五食堂']
df_filtered = df[df['Dept'].isin(canteens)]

# 分组统计每个时间段内各个食堂的就餐人数
time_period_canteen_counts = df_filtered.groupby(['时间段', 'Dept']).size().unstack(fill_value=0)

# 打印统计结果
print(time_period_canteen_counts)

# 确定高峰期
peak_periods = time_period_canteen_counts.idxmax(axis=0)
print("每个食堂的高峰期：")
for canteen, peak_period in peak_periods.items():
    print(f"{canteen}: {peak_period}")

# 设置字体
font_path = r"C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\OPPOSans-R.ttf"  # 请根据实际情况调整路径
try:
    font = FontProperties(fname=font_path)
except Exception as e:
    print(f"加载字体失败: {e}")
    font = None

# 设置全局字体配置
plt.rcParams['font.sans-serif'] = ['OPPOSans'] if font is None else [font.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 提高分辨率
plt.rcParams['figure.dpi'] = 150  # 设置图像分辨率为150 DPI

# 绘制三个饼图，每个时间段一个饼图
time_periods = ['早', '中', '晚']
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, time_period in enumerate(time_periods):
    ax = axes[i]
    canteen_counts = time_period_canteen_counts.loc[time_period]
    ax.pie(canteen_counts, labels=canteen_counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontproperties': font})
    ax.set_title(f'{time_period}时间段各个食堂的就餐人数占比', fontproperties=font)

plt.tight_layout()
plt.show()

######################

# 读取CSV文件并显示前几行和列名
file_path = r'C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\学生校园消费行为分析\data2.csv'
df = pd.read_csv(file_path, sep=',', encoding='gbk')

# 显示前几行数据
print(df.head())

# 显示列名
print(df.columns)

#将 Date 列转换为 datetime 类型
df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M')

#判断是否为工作日
# weekday() 返回的值为 0-6，0 表示周一，6 表示周日
df['是否工作日'] = df['Date'].dt.weekday < 5  # 0-4为工作日，5-6为周末

# 打印结果
print(df)

# 显示数据类型
print(df.dtypes)

# 检查并过滤掉无效的日期值
invalid_dates = df[df['Date'].isna()]
print("无效日期的数量:", invalid_dates.shape[0])
print("无效日期的具体值:")
print(invalid_dates['Date'].head())

# 查看无效日期的具体值
print("无效日期的详细信息:")
print(invalid_dates.head(10))

# 过滤掉无效的日期值
df = df.dropna(subset=['Date'])

# 再次检查数据类型，确保Date列已经转换为datetime类型
if df['Date'].dtype == 'datetime64[ns]':
    print("Date列已经成功转换为datetime类型")
else:
    print("Date列转换失败，仍然为object类型")

# 添加一列标识工作日和非工作日
df['是否工作日'] = df['Date'].dt.weekday < 5  # 0-4为工作日，5-6为周末

# 按小时统计就餐人数
df['小时'] = df['Date'].dt.hour

# 分组统计工作日和非工作日的每小时就餐人数
workday_counts = df[df['是否工作日']].groupby('小时').size()
non_workday_counts = df[~df['是否工作日']].groupby('小时').size()

# 绘制工作日和非工作日的食堂就餐时间曲线图
plt.figure(figsize=(10, 6))
plt.plot(workday_counts.index, workday_counts.values, label='工作日')
plt.plot(non_workday_counts.index, non_workday_counts.values, label='非工作日')
plt.xlabel('小时', fontproperties=font)
plt.ylabel('就餐人数', fontproperties=font)
plt.title('工作日和非工作日食堂就餐时间曲线图', fontproperties=font)
plt.legend()
plt.grid(True)
plt.show()

#######早中晚
# 定义时间段
def get_time_period(hour):
    if 6 <= hour < 10:
        return '早'
    elif 10 <= hour < 17:
        return '中'
    else:
        return '晚'

# 添加时间段列
df['时间段'] = df['Date'].dt.hour.apply(get_time_period)

# 过滤只包含 canteen1 到 canteen5 的记录
canteens = ['第一食堂', '第二食堂', '第三食堂', '第四食堂', '第五食堂']
df_filtered = df[df['Dept'].isin(canteens)]

# 分组统计每个时间段内各个食堂的就餐人数
time_period_canteen_counts = df_filtered.groupby(['时间段', 'Dept']).size().unstack(fill_value=0)

# 打印统计结果
print(time_period_canteen_counts)

# 绘制柱状图
time_period_canteen_counts.plot(kind='bar', figsize=(12, 8))
plt.xlabel('时间段', fontproperties=font)
plt.ylabel('就餐人数', fontproperties=font)
plt.title('早、中、晚时间段内各个食堂的就餐人数', fontproperties=font)
plt.legend(title='食堂', prop=font)
plt.grid(True)
plt.show()

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


# 打印高消费群体和低消费群体的平均消费金额
print("高消费群体平均消费金额:")
print(student_average_cost[student_average_cost > threshold].describe())

print("低消费群体平均消费金额:")
print(student_average_cost[student_average_cost <= threshold].describe())

# 统计低消费群体在不同消费地点的消费次数
low_spending_counts = low_spending['Dept'].value_counts()

# 检查数据是否为空
if low_spending_counts.empty:
    print("低消费群体数据为空")
else:
    print("低消费群体消费地点分布:")
    print(low_spending_counts)

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
