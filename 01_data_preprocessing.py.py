import pandas as pd
import numpy as np

# 读取数据
data1 = pd.read_csv(r'C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\学生校园消费行为分析\data1.csv', sep=',', encoding='gbk')
data2 = pd.read_csv(r'C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\学生校园消费行为分析\data2.csv', sep=',', encoding='gbk')
data3 = pd.read_csv(r'C:\Users\DELL\Desktop\数字图书馆关键技术期末作业-20250108\学生校园消费行为分析\data3.csv', sep=',', encoding='gbk')

# 定义一个函数来检测和处理缺失值
def detect_and_handle_missing_values(df):
    # 打印缺失值情况
    print("缺失值检测结果：")
    print(df.isna().sum())

    # 使用线性插值法填充缺失值
    df.interpolate(method='linear', inplace=True)

    return df

# 定义一个函数来检测和处理异常值
def detect_and_handle_outliers(df):
    # 选择数值类型的列
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    # 计算IQR
    Q1 = df[numeric_cols].quantile(0.25)
    Q3 = df[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1

    # 定义异常值的范围
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # 检测异常值
    outliers = (df[numeric_cols] < lower_bound) | (df[numeric_cols] > upper_bound)

    # 打印异常值
    print("异常值检测结果：")
    print(outliers.sum())

    # 处理异常值：用中位数替换
    df[numeric_cols] = df[numeric_cols].where(~outliers, df[numeric_cols].median(), axis=1)

    return df

# 对 data1、data2 和 data3 进行缺失值和异常值的检测和处理
data1 = detect_and_handle_missing_values(data1)
data1 = detect_and_handle_outliers(data1)

data2 = detect_and_handle_missing_values(data2)
data2 = detect_and_handle_outliers(data2)

data3 = detect_and_handle_missing_values(data3)
data3 = detect_and_handle_outliers(data3)

# 将处理后的数据保存到指定文件名
datasets = [data1, data2, data3]
for i, df in enumerate(datasets, start=1):
    df.to_csv(f'C:/Users/DELL/Desktop/数字图书馆关键技术期末作业-20250108/学生校园消费行为分析/task_1_1_{i}.csv', index=False, encoding='utf-8-sig')
    print(f"处理完成，结果已保存为 task_1_1_{i}.csv")

# 将 data1 与 data2 进行关联
merged_data1_2 = pd.merge(data1, data2, on='CardNo', how='inner')

# 将 data1 与 data3 进行关联
merged_data1_3 = pd.merge(data1, data3, on='AccessCardNo', how='inner')

# 保存结果
merged_data1_2.to_csv('C:/Users/DELL/Desktop/数字图书馆关键技术期末作业-20250108/学生校园消费行为分析/task1_2_1.csv', index=False, encoding='utf-8-sig')
merged_data1_3.to_csv('C:/Users/DELL/Desktop/数字图书馆关键技术期末作业-20250108/学生校园消费行为分析/task1_2_2.csv', index=False, encoding='utf-8-sig')
print("处理完成，结果已保存为 task1_2_1.csv 和 task1_2_2.csv")
