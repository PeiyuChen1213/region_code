# 批量讲csv文件转成excel的xlsx

import os
import pandas as pd

# 指定CSV文件夹和XLSX文件夹路径
csv_folder = 'C:\\Users\\29844\Desktop\\region_code'
xlsx_folder = 'C:\\Users\\29844\\Desktop\\region_code2'

# 确保保存XLSX的文件夹存在
os.makedirs(xlsx_folder, exist_ok=True)

# 遍历CSV文件夹中的所有文件
for csv_file in os.listdir(csv_folder):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_folder, csv_file)
        xlsx_file = os.path.splitext(csv_file)[0] + '.xlsx'
        xlsx_path = os.path.join(xlsx_folder, xlsx_file)

        # 读取CSV文件的表头
        with open(csv_path, 'r', encoding='gbk') as f:
            header = f.readline().strip().split(',')

        # 读取CSV文件内容，跳过表头
        df = pd.read_csv(csv_path, encoding='gbk',skiprows=[0])

        # 将表头添加到XLSX文件中
        writer = pd.ExcelWriter(xlsx_path, engine='xlsxwriter')
        df.to_excel(writer, index=False, header=False, startrow=1)

        # 获取XLSX写入对象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # 将表头写入XLSX文件
        for col_num, value in enumerate(header):
            worksheet.write(0, col_num, value)

        # 关闭写入对象
        writer._save()

        print(f"Converted {csv_file} to {xlsx_file}")

print("Conversion completed!")