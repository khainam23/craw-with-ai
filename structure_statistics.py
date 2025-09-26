#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để thống kê field "structure" từ file crawl_results_20250926_143534.json
"""

import json
from collections import Counter
import os

def analyze_structure_field(json_file_path):
    """
    Phân tích field "structure" trong file JSON
    
    Args:
        json_file_path (str): Đường dẫn đến file JSON
    
    Returns:
        dict: Thống kê về field structure
    """
    
    # Đọc file JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {json_file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Lỗi đọc file JSON: {e}")
        return None
    
    # Kiểm tra dữ liệu
    if not isinstance(data, list):
        print("Dữ liệu không phải là một danh sách")
        return None
    
    # Thu thập tất cả giá trị của field "structure"
    structure_values = []
    total_records = len(data)
    records_with_structure = 0
    
    for record in data:
        if isinstance(record, dict) and 'structure' in record:
            structure_values.append(record['structure'])
            records_with_structure += 1
    
    # Thống kê
    structure_counter = Counter(structure_values)
    
    # Tạo kết quả thống kê
    statistics = {
        'total_records': total_records,
        'records_with_structure': records_with_structure,
        'records_without_structure': total_records - records_with_structure,
        'unique_structure_values': len(structure_counter),
        'structure_distribution': dict(structure_counter),
        'structure_percentages': {}
    }
    
    # Tính phần trăm cho mỗi loại structure
    for structure_type, count in structure_counter.items():
        percentage = (count / records_with_structure) * 100 if records_with_structure > 0 else 0
        statistics['structure_percentages'][structure_type] = round(percentage, 2)
    
    return statistics

def save_statistics_to_file(statistics, output_file):
    """
    Lưu thống kê vào file
    
    Args:
        statistics (dict): Dữ liệu thống kê
        output_file (str): Đường dẫn file output
    """
    
    if not statistics:
        print("Không có dữ liệu thống kê để lưu")
        return
    
    # Tạo nội dung báo cáo
    report_content = []
    report_content.append("=" * 60)
    report_content.append("THỐNG KÊ FIELD 'STRUCTURE' - CRAWL RESULTS")
    report_content.append("=" * 60)
    report_content.append("")
    
    # Thông tin tổng quan
    report_content.append("1. THÔNG TIN TỔNG QUAN:")
    report_content.append(f"   - Tổng số bản ghi: {statistics['total_records']:,}")
    report_content.append(f"   - Số bản ghi có field 'structure': {statistics['records_with_structure']:,}")
    report_content.append(f"   - Số bản ghi không có field 'structure': {statistics['records_without_structure']:,}")
    report_content.append(f"   - Số loại structure khác nhau: {statistics['unique_structure_values']}")
    report_content.append("")
    
    # Phân bố structure
    report_content.append("2. PHÂN BỐ CÁC LOẠI STRUCTURE:")
    report_content.append("-" * 40)
    
    # Sắp xếp theo số lượng giảm dần
    sorted_structures = sorted(statistics['structure_distribution'].items(), 
                              key=lambda x: x[1], reverse=True)
    
    for structure_type, count in sorted_structures:
        percentage = statistics['structure_percentages'].get(structure_type, 0)
        report_content.append(f"   {structure_type:<15}: {count:>6,} bản ghi ({percentage:>6.2f}%)")
    
    report_content.append("")
    
    # Thống kê chi tiết
    report_content.append("3. THỐNG KÊ CHI TIẾT:")
    report_content.append("-" * 40)
    
    if statistics['records_with_structure'] > 0:
        coverage_percentage = (statistics['records_with_structure'] / statistics['total_records']) * 100
        report_content.append(f"   - Tỷ lệ bản ghi có field 'structure': {coverage_percentage:.2f}%")
    
    # Tìm structure phổ biến nhất
    if sorted_structures:
        most_common = sorted_structures[0]
        report_content.append(f"   - Structure phổ biến nhất: '{most_common[0]}' ({most_common[1]:,} bản ghi)")
    
    # Tìm structure ít phổ biến nhất
    if len(sorted_structures) > 1:
        least_common = sorted_structures[-1]
        report_content.append(f"   - Structure ít phổ biến nhất: '{least_common[0]}' ({least_common[1]:,} bản ghi)")
    
    report_content.append("")
    report_content.append("=" * 60)
    report_content.append("Báo cáo được tạo bởi structure_statistics.py")
    report_content.append("=" * 60)
    
    # Lưu vào file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
        print(f"Đã lưu báo cáo thống kê vào: {output_file}")
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

def save_json_statistics(statistics, output_file):
    """
    Lưu thống kê dưới dạng JSON
    
    Args:
        statistics (dict): Dữ liệu thống kê
        output_file (str): Đường dẫn file JSON output
    """
    
    if not statistics:
        print("Không có dữ liệu thống kê để lưu")
        return
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(statistics, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu thống kê JSON vào: {output_file}")
    except Exception as e:
        print(f"Lỗi khi lưu file JSON: {e}")

def main():
    """Hàm main"""
    
    # Đường dẫn file input
    input_file = "crawl_results_20250926_145718.json"
    
    # Kiểm tra file tồn tại
    if not os.path.exists(input_file):
        print(f"Không tìm thấy file: {input_file}")
        return
    
    print("Đang phân tích dữ liệu...")
    
    # Phân tích dữ liệu
    statistics = analyze_structure_field(input_file)
    
    if not statistics:
        print("Không thể phân tích dữ liệu")
        return
    
    # Hiển thị kết quả trên console
    print("\n" + "="*50)
    print("KẾT QUẢ THỐNG KÊ FIELD 'STRUCTURE'")
    print("="*50)
    print(f"Tổng số bản ghi: {statistics['total_records']:,}")
    print(f"Bản ghi có field 'structure': {statistics['records_with_structure']:,}")
    print(f"Số loại structure: {statistics['unique_structure_values']}")
    print("\nPhân bố structure:")
    
    sorted_structures = sorted(statistics['structure_distribution'].items(), 
                              key=lambda x: x[1], reverse=True)
    
    for structure_type, count in sorted_structures:
        percentage = statistics['structure_percentages'].get(structure_type, 0)
        print(f"  {structure_type:<15}: {count:>6,} ({percentage:>6.2f}%)")
    
    # Lưu báo cáo
    output_text_file = "structure_statistics_report.txt"
    output_json_file = "structure_statistics_data.json"
    
    save_statistics_to_file(statistics, output_text_file)
    save_json_statistics(statistics, output_json_file)
    
    print(f"\nĐã tạo các file báo cáo:")
    print(f"  - Báo cáo text: {output_text_file}")
    print(f"  - Dữ liệu JSON: {output_json_file}")

if __name__ == "__main__":
    main()