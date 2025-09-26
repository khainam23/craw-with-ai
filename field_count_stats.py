#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field Count Statistics
Thống kê count của từng field trong file JSON
"""

import json
from collections import Counter

def analyze_field_counts(json_file_path: str):
    """Thống kê từng field xuất hiện bao nhiều lần"""
    
    # Đọc file JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi đọc JSON: {e}")
        return
    
    if not isinstance(data, list):
        print("❌ Dữ liệu không phải là một array")
        return
    
    print("=" * 80)
    print("THỐNG KÊ COUNT CỦA TỪNG FIELD")
    print("=" * 80)
    
    # Đếm số lần xuất hiện của từng field
    field_counter = Counter()
    total_records = len(data)
    
    for record in data:
        if isinstance(record, dict):
            for field_name in record.keys():
                field_counter[field_name] += 1
    
    print(f"📊 TỔNG QUAN:")
    print(f"   • Tổng số records: {total_records}")
    print(f"   • Tổng số field unique: {len(field_counter)}")
    
    print(f"\n📈 COUNT CỦA TỪNG FIELD:")
    print(f"{'Field Name':<35} {'Count':<8} {'Percentage':<12}")
    print("-" * 80)
    
    # Sắp xếp theo tên field
    for field_name in sorted(field_counter.keys()):
        count = field_counter[field_name]
        percentage = (count / total_records) * 100
        print(f"{field_name:<35} {count:<8} {percentage:>8.1f}%")
    
    print("=" * 80)

def main():
    """Hàm main"""
    json_file = "crawl_results_20250926_023546.json"
    analyze_field_counts(json_file)

if __name__ == "__main__":
    main()