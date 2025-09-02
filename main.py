# -*- coding: utf-8 -*-
import subprocess
import sys

def run_script(script_name):
    """
    调用指定的Python脚本
    """
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(f"\n===== 执行 {script_name} 输出 =====")
    print(result.stdout)
    if result.stderr:
        print(f"\n[WARNING] {script_name} 错误输出:")
        print(result.stderr)

if __name__ == "__main__":
    print("=" * 60)
    print("车辆信息批量OCR识别与Excel导出工具")
    print("=" * 60)
    print("\n[1] 开始执行OCR识别(ocr_main.py)...")
    run_script("ocr_main.py")
    print("\n[2] 开始提取JSON并导出Excel(jsontoexecl.py)...")
    run_script("jsontoexecl.py")
    print("\n全部流程执行完成!")
