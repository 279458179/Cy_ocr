#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例运行脚本
演示如何使用Cy_OCR进行车辆信息识别
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def run_ocr_example():
    """运行OCR识别示例"""
    print("=" * 60)
    print("Cy_OCR 示例运行脚本")
    print("=" * 60)
    
    # 检查输入目录
    input_dir = project_root / "images_input"
    if not input_dir.exists():
        print(f"输入目录不存在: {input_dir}")
        print("请将图片文件放入 images_input/ 目录中")
        return False
    
    # 检查是否有图片文件
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        image_files.extend(input_dir.glob(f"*{ext}"))
        image_files.extend(input_dir.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"在 {input_dir} 中没有找到图片文件")
        print("支持的格式: .jpg, .jpeg, .png, .bmp, .tiff")
        return False
    
    print(f"找到 {len(image_files)} 个图片文件:")
    for img_file in image_files:
        print(f"  - {img_file.name}")
    
    # 运行OCR识别
    print("\n开始OCR识别...")
    try:
        from ocr_main import main as ocr_main
        ocr_main()
        print("OCR识别完成！")
    except Exception as e:
        print(f"OCR识别失败: {e}")
        return False
    
    # 运行Excel导出
    print("\n开始Excel导出...")
    try:
        from jsontoexecl import main as excel_main
        excel_main()
        print("Excel导出完成！")
    except Exception as e:
        print(f"Excel导出失败: {e}")
        return False
    
    print("\n示例运行完成！")
    print("请查看以下文件:")
    print(f"  - Excel文件: {project_root / '车辆信息提取结果.xlsx'}")
    print(f"  - 输出目录: {project_root / 'output'}")
    
    return True

if __name__ == "__main__":
    success = run_ocr_example()
    if not success:
        sys.exit(1)


