#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件示例
复制此文件为 config.py 并根据需要修改配置
"""

# OCR配置
OCR_CONFIG = {
    # 是否使用文档方向分类
    'use_doc_orientation_classify': False,
    
    # 是否使用文档去弯曲
    'use_doc_unwarping': False,
    
    # 是否使用GPU加速（需要安装paddlepaddle-gpu）
    'use_gpu': False,
    
    # GPU设备ID（如果使用GPU）
    'gpu_id': 0,
}

# 文件路径配置
PATH_CONFIG = {
    # 输入图片目录
    'input_dir': 'images_input',
    
    # 输出结果目录
    'output_dir': 'output',
    
    # Excel输出文件名
    'excel_filename': '车辆信息提取结果.xlsx',
    
    # CSV输出文件名（备用）
    'csv_filename': '车辆信息提取结果.csv',
}

# 支持的图片格式
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

# Excel字段顺序配置
EXCEL_FIELD_ORDER = [
    '号牌种类', '号牌号码', '车辆类型', '使用性质', '车辆品牌',
    '初次登记日期', '有效期至', '强制报废期止', '车辆识别代号',
    '发动机号', '行驶证编号', '发证机关', '违法未处理次数',
    '车辆状态', '车身颜色', '联系电话', '核定载客人数',
    '所有人', '联系地址'
]

# 日志配置
LOG_CONFIG = {
    # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
    'level': 'INFO',
    
    # 日志文件路径
    'file_path': 'ocr.log',
    
    # 日志格式
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}


