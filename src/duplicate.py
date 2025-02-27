import pandas as pd

# 读取Excel文件
df = pd.read_excel('C:/Users/mengl/Desktop/dsproject/data/raw/raw.xlsx')

# 按行去重（保留第一个出现的行）
df.drop_duplicates(inplace=True)

# 保存结果
df.to_excel('C:/Users/mengl/Desktop/dsproject/data/outputs/result.xlsx', index=False)