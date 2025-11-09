'''
Author: Diana Tang
'''
import pandas as pd

# 1. 读取 CSV 文件
df = pd.read_csv("csv-NatureJour-set.csv")

# 2. 查看有哪些列可用于判断重复（可选）
print("列名：", df.columns.tolist())

# 3. 去重
# 如果文件中有唯一标识列（比如 PMID、Title 等），可以指定 subset
# 例如 subset=['PMID'] 或 ['Title', 'Authors']
df_dedup = df.drop_duplicates(subset=['Title'], keep='first')

# 4. 输出去重后的结果
output_path = "csv-NatureJour-set-dedup.csv"
df_dedup.to_csv(output_path, index=False)

print(f"✅ 去重完成，已保存到 {output_path}，原始记录数：{len(df)}，去重后：{len(df_dedup)}")
