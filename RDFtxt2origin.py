# RDF txt convert to Origin
#Created by LRZ
#version 1.0 2025.2.21

import os
import pandas as pd
import glob

# 获取当前的工作文件夹
file_path = os.getcwd()
files = glob.glob(file_path + '/*.txt')  # 获取所有的 txt 文件

dfs = []

# 在 for 循环中将排序函数进行修改，以文件名数字排序
for file in sorted(files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0])):
    file_name = os.path.basename(file)  # 获取文件名
    file_name_without_extension = os.path.splitext(file_name)[0]  # 移除扩展名
    temp_df = pd.read_csv(file, delim_whitespace=True, header=None) # 从文件中读取数据
    # 将第二列重命名为处理过的文件名（数字部分）
    temp_df = temp_df.rename(columns={1: file_name_without_extension})
    dfs.append(temp_df)

# 使用文件中的第一列（即列0）作为key，将所有数据合并起来
merged_df = pd.concat(dfs, axis=1)
# drop duplicate columns based on column name
merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

# 将结果写入新的 txt 文件
merged_df.to_csv(file_path + '/output.txt', sep='\t', index=False)
