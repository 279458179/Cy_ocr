#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从output目录下的JSON文件中提取rec_texts字段数据, 生成Excel表格
"""

import json
import os
import pandas as pd
from pathlib import Path

def parse_rec_texts(rec_texts):
    """
    解析rec_texts列表, 将键值对提取为字典
    """
    data = {}
    i = 0
    while i < len(rec_texts) - 1:
        key = rec_texts[i]
        value = rec_texts[i + 1]
        
        # 跳过纯数字的项(如"1", "3"等)
        if key.isdigit():
            i += 1
            continue
            
        data[key] = value
        i += 2
    
    return data

def process_json_files():
    """
    处理output目录下的所有JSON文件
    """
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("output目录不存在!")
        return
    
    # 存储所有提取的数据
    all_data = []
    
    # 递归遍历output目录下的所有json文件(包括子目录)
    json_files = list(output_dir.rglob("*.json"))
    
    if not json_files:
        print("output目录下没有找到JSON文件!")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件, 开始处理...")
    
    for json_file in json_files:
        relative_path = json_file.relative_to(output_dir)
        print(f"正在处理: {relative_path}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取rec_texts字段(可能嵌套在overall_ocr_res中)
            rec_texts = None
            
            # 首先检查根层级
            if 'rec_texts' in data:
                rec_texts = data['rec_texts']
            # 然后检查是否在overall_ocr_res中
            elif 'overall_ocr_res' in data and 'rec_texts' in data['overall_ocr_res']:
                rec_texts = data['overall_ocr_res']['rec_texts']
            
            if rec_texts:
                parsed_data = parse_rec_texts(rec_texts)
                
                # 添加文件路径信息(包含相对路径)
                parsed_data['源文件路径'] = str(json_file.relative_to(output_dir))
                
                all_data.append(parsed_data)
                print(f"  成功提取数据")
            else:
                print(f"  警告: {relative_path} 中未找到 'rec_texts' 字段")
                
        except json.JSONDecodeError as e:
            print(f"  错误: {relative_path} JSON格式错误 - {e}")
        except Exception as e:
            print(f"  错误: 处理 {relative_path} 时出错 - {e}")
    
    if not all_data:
        print("没有成功提取到任何数据!")
        return
    
    # 创建DataFrame
    df = pd.DataFrame(all_data)
    
    # 定义列的顺序(根据图片中的表头)
    desired_columns = [
        '号牌种类', '号牌号码', '车辆类型', '使用性质', '车辆品牌',
        '初次登记日期', '有效期至', '强制报废期止', '车辆识别代号',
        '发动机号', '行驶证编号', '发证机关', '违法未处理次数',
        '车辆状态', '车身颜色', '联系电话', '核定载客人数',
        '所有人', '联系地址'
    ]
    
    # 重新排列列的顺序, 确保所有列都存在
    existing_columns = [col for col in desired_columns if col in df.columns]
    missing_columns = [col for col in desired_columns if col not in df.columns]
    
    # 为缺失的列添加空值
    for col in missing_columns:
        df[col] = ''
    
    # 按照期望的顺序重新排列列
    df = df[desired_columns]
    
    # 保存到Excel文件
    output_file = "车辆信息提取结果.xlsx"
    try:
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"\n数据提取完成!")
        print(f"总共处理了 {len(all_data)} 条记录")
        print(f"结果已保存到: {output_file}")
        
        # 显示数据预览
        print(f"\n数据预览:")
        print(df.head())
        
    except Exception as e:
        print(f"保存Excel文件时出错: {e}")
        print("尝试保存为CSV格式...")
        try:
            csv_file = "车辆信息提取结果.csv"
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"CSV文件已保存到: {csv_file}")
        except Exception as csv_error:
            print(f"保存CSV文件也失败: {csv_error}")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("车辆信息JSON转Excel工具")
    print("=" * 60)
    
    # 检查必要的库
    try:
        import pandas as pd
        import openpyxl
    except ImportError as e:
        print(f"缺少必要的库: {e}")
        print("请运行以下命令安装依赖:")
        print("pip install pandas openpyxl")
        return
    
    process_json_files()
    print("\n程序执行完成!")

if __name__ == "__main__":
    main()