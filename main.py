import pandas as pd

# 读取t_org和area_code文件为DataFrame
t_org_df = pd.read_csv('t_org.csv', encoding='utf-8')
area_code_df = pd.read_csv('area_code.csv', encoding='utf-8')

# 将area_code_df的C1列中的浮点数值转换为字符串
area_code_df['c1'] = area_code_df['c1'].astype(str)

# 在area_code_df中创建一个新列，用于存储C1列的前六位
area_code_df['c1_prefix'] = area_code_df['c1'].str[:6]

# 创建一个字典用于存储匹配的short_name和对应的C1值
short_name_to_c1 = dict(zip(area_code_df['c2'], area_code_df['c1']))


# 定义一个函数用于根据short_name和region_code查找对应的C1值
def find_c1_value(row):
    short_name = str(row['short_name'])
    region_code = row['region_code']

    # 获取region_code的前六位
    region_code_prefix = str(region_code)[:6]

    # 检查short_name是否在字典中存在
    for key in short_name_to_c1:
        if key in short_name:
            c1_value = short_name_to_c1[key]
            if c1_value[:6] == region_code_prefix:
                return c1_value
            # return c1_value;
    return None


# 使用apply函数在t_org_df中添加新列，根据short_name和region_code匹配C1值，并转换为字符串
t_org_df['new_column'] = t_org_df.apply(find_c1_value, axis=1).astype(str)

# 将修改后的t_org_df保存到新文件
t_org_df.to_csv('t_org_updated.csv', index=False, encoding='utf-8')
