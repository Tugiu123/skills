#!/usr/bin/env python3
"""
Excel2Insights - Excel数据分析工具
版本: v1.0.8
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
import argparse
from datetime import datetime

class ExcelAnalyzer:
    def __init__(self):
        self.data = None
    
    def load_data(self, file_path):
        """加载Excel数据"""
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)
            return True
        except Exception as e:
            print(f"加载文件失败: {e}")
            return False
    
    def analyze(self):
        """执行数据分析"""
        if self.data is None:
            print("请先加载数据")
            return
        
        print("数据概览:")
        print(f"行数: {len(self.data)}")
        print(f"列数: {len(self.data.columns)}")
        print(f"数据类型:")
        print(self.data.dtypes)
    
    def save_report(self, output_path):
        """保存分析报告"""
        if self.data is None:
            print("无数据可报告")
            return
        
        with open(output_path, 'w') as f:
            f.write(f"Excel数据分析报告\n")
            f.write(f"生成时间: {datetime.now()}\n")
            f.write(f"数据行数: {len(self.data)}\n")
            f.write(f"数据列数: {len(self.data.columns)}\n")
        
        print(f"报告已保存到: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Excel数据分析工具')
    parser.add_argument('--file', help='Excel文件路径')
    parser.add_argument('--analyze', action='store_true', help='执行分析')
    parser.add_argument('--output', default='./output/report.txt', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.file:
        analyzer = ExcelAnalyzer()
        if analyzer.load_data(args.file):
            if args.analyze:
                analyzer.analyze()
                analyzer.save_report(args.output)
        else:
            print("无法加载文件")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
