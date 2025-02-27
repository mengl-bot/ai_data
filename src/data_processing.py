import pandas as pd
import os

def process_inventory_data():
    # 路径配置
    input_path = '../data/raw/库存明细报表.xlsx'
    output_dir = '../output/'
    output_file = 'processed_inventory.xlsx'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取原始数据
    df = pd.read_excel(input_path)
    
    # 处理数据：去重后统计库位数量
    unique_df = df.drop_duplicates(['物流编码', '商品编码', '库位编码'])
    
    # 生成第一个结果：每个物流编码下超过5个库位的商品
    # 计算每个物流+商品的库位数量
    loc_count = unique_df.groupby(['物流编码', '商品编码'])['库位编码'].nunique().reset_index()
    over_5_locations = loc_count[loc_count['库位编码'] > 5]
    
    # 合并原始数据获取完整记录
    result1 = pd.merge(over_5_locations, unique_df, 
                      on=['物流编码', '商品编码'],
                      how='left')
    
    # 生成第二个结果：各站点超过5个库位的商品数量
    # 按仓库（站点）统计
    warehouse_stats = (unique_df.groupby(['仓库编码', '商品编码'])['库位编码']
                       .nunique()
                       .reset_index()
                       .query('库位编码 > 5')
                       .groupby('仓库编码')['商品编码']
                       .nunique()
                       .reset_index(name='超标商品数量'))
    
    # 保存结果到不同sheet
    with pd.ExcelWriter(os.path.join(output_dir, output_file)) as writer:
        result1.to_excel(writer, sheet_name='超标商品明细', index=False)
        warehouse_stats.to_excel(writer, sheet_name='站点统计', index=False)

if __name__ == "__main__":
    process_inventory_data() 