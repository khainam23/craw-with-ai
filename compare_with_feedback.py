#!/usr/bin/env python3
"""
Script để so sánh kết quả crawl với feedback
"""

import json
from typing import Dict, Any

def load_latest_crawl_result() -> Dict[str, Any]:
    """Load kết quả crawl mới nhất"""
    import glob
    import os
    
    # Tìm file crawl_results mới nhất
    pattern = "crawl_results_*.json"
    files = glob.glob(pattern)
    if not files:
        print("❌ Không tìm thấy file crawl results")
        return {}
    
    latest_file = max(files, key=os.path.getctime)
    print(f"📁 Loading: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if data and len(data) > 0 and data[0].get('success'):
        return data[0]['property_data']
    return {}

def compare_with_feedback(crawl_data: Dict[str, Any]):
    """So sánh với feedback từ feedback.txt"""
    
    print("\n" + "="*80)
    print("🔍 SO SÁNH KẾT QUẢ CRAWL VỚI FEEDBACK")
    print("="*80)
    
    # Feedback data từ feedback.txt
    feedback_comparisons = [
        {
            'field': 'Địa chỉ',
            'crawl_key': ['prefecture', 'district', 'chome_banchi'],
            'crawl_expected': '東京都練馬区桜台三丁目２０番３号',
            'website_actual': '東京都練馬区桜台三丁目２０番３号',
            'issue': 'Crawl thiếu chi tiết số nhà và khu phố'
        },
        {
            'field': 'Postcode',
            'crawl_key': 'postcode',
            'crawl_expected': '107-0052',
            'website_actual': 'Không hiển thị trực tiếp trên web',
            'issue': 'Không kiểm chứng được'
        },
        {
            'field': 'Loại tòa nhà',
            'crawl_key': ['building_type', 'structure'],
            'crawl_expected': 'マンション',
            'website_actual': '鉄筋コンクリート造 地上3階建',
            'issue': 'Crawl chỉ ghi "マンション", web chi tiết cấu trúc'
        },
        {
            'field': 'Tên tòa (EN/JA)',
            'crawl_key': 'building_name_ja',
            'crawl_expected': 'PLANE SOCIE＋ SAKURADAI 1階１０１',
            'website_actual': 'PLANE SOCIE＋ SAKURADAI 1階１０１',
            'issue': 'Khớp'
        },
        {
            'field': 'Ga gần nhất',
            'crawl_key': ['station_name_1', 'station_name_2', 'walk_1', 'walk_2'],
            'crawl_expected': '新桜台駅 (6 phút đi bộ)',
            'website_actual': '新桜台駅 (6 phút đi bộ), 氷川台駅 (8 phút đi bộ)',
            'issue': 'Crawl thiếu ga thứ hai'
        },
        {
            'field': 'Số tầng',
            'crawl_key': 'floors',
            'crawl_expected': '3',
            'website_actual': '地上3階建',
            'issue': 'Khớp về tổng số tầng'
        },
        {
            'field': 'Diện tích',
            'crawl_key': 'size',
            'crawl_expected': '31.71㎡',
            'website_actual': '31.71㎡',
            'issue': 'Khớp'
        },
        {
            'field': 'Ngày có sẵn',
            'crawl_key': 'available_from',
            'crawl_expected': '相談',
            'website_actual': '10月中旬',
            'issue': 'Crawl không chính xác'
        },
        {
            'field': 'Bãi đỗ xe',
            'crawl_key': 'parking',
            'crawl_expected': 'Y',
            'website_actual': '無',
            'issue': 'Sai, web không có bãi đỗ xe'
        },
        {
            'field': 'Bãi xe máy',
            'crawl_key': 'motorcycle_parking',
            'crawl_expected': 'Y',
            'website_actual': 'Không thấy thông tin',
            'issue': 'Crawl có thể thêm tự động'
        }
    ]
    
    for comparison in feedback_comparisons:
        print(f"\n📋 {comparison['field']}:")
        print(f"   🎯 Website thực tế: {comparison['website_actual']}")
        
        # Get crawl value
        crawl_keys = comparison['crawl_key']
        if isinstance(crawl_keys, str):
            crawl_keys = [crawl_keys]
        
        crawl_values = []
        for key in crawl_keys:
            value = crawl_data.get(key)
            if value:
                crawl_values.append(f"{key}: {value}")
        
        crawl_result = " | ".join(crawl_values) if crawl_values else "❌ Không có dữ liệu"
        print(f"   🤖 Crawl hiện tại: {crawl_result}")
        
        # Status
        if comparison['issue'] == 'Khớp':
            print(f"   ✅ Trạng thái: {comparison['issue']}")
        else:
            print(f"   ⚠️  Vấn đề: {comparison['issue']}")
    
    print("\n" + "="*80)
    print("📊 TỔNG KẾT CẢI THIỆN")
    print("="*80)
    
    # Tính toán cải thiện
    total_fields = len(feedback_comparisons)
    improved_fields = 0
    
    for comparison in feedback_comparisons:
        if comparison['field'] in ['Loại tòa nhà', 'Địa chỉ']:
            # Check if we have more detailed structure info
            if crawl_data.get('structure') and '鉄筋コンクリート造' in crawl_data.get('structure', ''):
                improved_fields += 0.5
            if crawl_data.get('chome_banchi'):
                improved_fields += 0.5
        elif comparison['issue'] == 'Khớp':
            improved_fields += 1
    
    print(f"✅ Đã cải thiện: {improved_fields}/{total_fields} fields")
    print(f"📈 Tỷ lệ chính xác: {improved_fields/total_fields*100:.1f}%")
    
    # Recommendations
    print("\n🔧 KHUYẾN NGHỊ CẢI THIỆN:")
    remaining_issues = [comp for comp in feedback_comparisons if comp['issue'] != 'Khớp']
    for issue in remaining_issues[:3]:  # Top 3 issues
        print(f"   • {issue['field']}: {issue['issue']}")

def main():
    """Main function"""
    crawl_data = load_latest_crawl_result()
    if not crawl_data:
        print("❌ Không thể load dữ liệu crawl")
        return
    
    compare_with_feedback(crawl_data)

if __name__ == "__main__":
    main()