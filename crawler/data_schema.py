"""
Schema và cấu trúc dữ liệu cho Property Crawler
"""

from datetime import datetime
from typing import Dict, Any


class PropertyDataSchema:
    """Schema cho dữ liệu property"""
    
    @staticmethod
    def get_empty_property_data(url: str) -> Dict[str, Any]:
        """
        Tạo cấu trúc dữ liệu property rỗng với tất cả fields
        """
        return {
            # Thông tin cơ bản
            'link': url,
            'property_csv_id': None,
            'create_date': datetime.now().isoformat(),
            
            # Địa chỉ
            'postcode': None,
            'prefecture': None,
            'city': None,
            'district': None,
            'chome_banchi': None,
            
            # Thông tin tòa nhà
            'building_type': None,
            'year': None,
            
            # Tên tòa nhà đa ngôn ngữ
            'building_name_en': None,
            'building_name_ja': None,
            'building_name_vi': None,
            
            # Mô tả tòa nhà đa ngôn ngữ
            'building_description_en': None,
            'building_description_ja': None,
            'building_description_vi': None,
            
            # Địa danh gần đó đa ngôn ngữ
            'building_landmarks_en': None,
            'building_landmarks_ja': None,
            'building_landmarks_vi': None,
            
            # Thông tin ga tàu (5 ga)
            'station_name_1': None, 'train_line_name_1': None, 'walk_1': None, 'bus_1': None, 'car_1': None, 'cycle_1': None,
            'station_name_2': None, 'train_line_name_2': None, 'walk_2': None, 'bus_2': None, 'car_2': None, 'cycle_2': None,
            'station_name_3': None, 'train_line_name_3': None, 'walk_3': None, 'bus_3': None, 'car_3': None, 'cycle_3': None,
            'station_name_4': None, 'train_line_name_4': None, 'walk_4': None, 'bus_4': None, 'car_4': None, 'cycle_4': None,
            'station_name_5': None, 'train_line_name_5': None, 'walk_5': None, 'bus_5': None, 'car_5': None, 'cycle_5': None,
            
            # Tọa độ địa lý
            'map_lat': None,
            'map_lng': None,
            
            # Thông tin cấu trúc tòa nhà
            'num_units': None,
            'floors': None,
            'basement_floors': None,
            
            # Thông tin đậu xe
            'parking': None,
            'parking_cost': None,
            'bicycle_parking': None,
            'motorcycle_parking': None,
            
            # Thông tin cấu trúc và phong cách
            'structure': None,
            'building_notes': None,
            'building_style': None,
            
            # Tiện ích tòa nhà
            'autolock': None, 'credit_card': None, 'concierge': None, 'delivery_box': None,
            'elevator': None, 'gym': None, 'newly_built': None, 'pets': None,
            'swimming_pool': None, 'ur': None,
            
            # Thông tin căn hộ
            'room_type': None,
            'size': None,
            'unit_no': None,
            'ad_type': None,
            'available_from': None,
            
            # Mô tả bất động sản đa ngôn ngữ
            'property_description_en': None,
            'property_description_ja': None,
            'property_description_vi': None,
            
            # Chi phí khác đa ngôn ngữ
            'property_other_expenses_en': None,
            'property_other_expenses_ja': None,
            'property_other_expenses_vi': None,
            
            # Loại nổi bật
            'featured_a': None, 'featured_b': None, 'featured_c': None,
            
            # Thông tin tầng và giá thuê
            'floor_no': None,
            'monthly_rent': None,
            'monthly_maintenance': None,
            
            # Các khoản phí
            'months_deposit': None, 'numeric_deposit': None,
            'months_key': None, 'numeric_key': None,
            'months_guarantor': None, 'numeric_guarantor': None,
            'months_agency': None, 'numeric_agency': None,
            'months_renewal': None, 'numeric_renewal': None,
            'months_deposit_amortization': None, 'numeric_deposit_amortization': None,
            'months_security_deposit': None, 'numeric_security_deposit': None,
            
            # Các phí khác
            'lock_exchange': None,
            'fire_insurance': None,
            'other_initial_fees': None,
            'other_subscription_fees': None,
            
            # Thông tin bảo lãnh
            'no_guarantor': None,
            'guarantor_agency': None,
            'guarantor_agency_name': None,
            'numeric_guarantor_max': None,
            
            # Thông tin thuê
            'rent_negotiable': None,
            'renewal_new_rent': None,
            'lease_date': None,
            'lease_months': None,
            'lease_type': None,
            'short_term_ok': None,
            
            # Thông tin ban công và ghi chú
            'balcony_size': None,
            'property_notes': None,
            'discount': None,
            
            # Hướng căn hộ
            'facing_north': None, 'facing_northeast': None, 'facing_east': None, 'facing_southeast': None,
            'facing_south': None, 'facing_southwest': None, 'facing_west': None, 'facing_northwest': None,
            
            # Tiện nghi căn hộ (rất nhiều)
            'aircon': None, 'aircon_heater': None, 'all_electric': None, 'auto_fill_bath': None,
            'balcony': None, 'bath': None, 'bath_water_heater': None, 'blinds': None,
            'bs': None, 'cable': None, 'carpet': None, 'cleaning_service': None,
            'counter_kitchen': None, 'dishwasher': None, 'drapes': None, 'female_only': None,
            'fireplace': None, 'flooring': None, 'full_kitchen': None, 'furnished': None,
            'gas': None, 'induction_cooker': None, 'internet_broadband': None, 'internet_wifi': None,
            'japanese_toilet': None, 'linen': None, 'loft': None, 'microwave': None,
            'oven': None, 'phoneline': None, 'range': None, 'refrigerator': None,
            'refrigerator_freezer': None, 'roof_balcony': None, 'separate_toilet': None, 'shower': None,
            'soho': None, 'storage': None, 'student_friendly': None, 'system_kitchen': None,
            'tatami': None, 'underfloor_heating': None, 'unit_bath': None, 'utensils_cutlery': None,
            'veranda': None, 'washer_dryer': None, 'washing_machine': None, 'washlet': None,
            'western_toilet': None, 'yard': None,
            
            # Media links
            'youtube': None,
            'vr_link': None,
            
            # Hình ảnh
            'images': []
        }


class AmenityKeywords:
    """Keywords cho việc detect amenities"""
    
    AMENITY_KEYWORDS = {
        # Building amenities
        'elevator': ['エレベーター', 'elevator', 'EV'],
        'autolock': ['オートロック', 'auto lock', 'autoloc'],
        'delivery_box': ['宅配ボックス', 'delivery box', '宅配BOX'],
        'concierge': ['コンシェルジュ', 'concierge', 'フロント'],
        'gym': ['ジム', 'gym', 'フィットネス'],
        'swimming_pool': ['プール', 'pool', 'swimming'],
        
        # Parking
        'parking': ['駐車場', 'parking', '駐車'],
        'bicycle_parking': ['駐輪場', 'bicycle parking', '自転車'],
        'motorcycle_parking': ['バイク置場', 'motorcycle', 'バイク'],
        
        # Unit amenities
        'aircon': ['エアコン', 'air conditioning', 'aircon', 'AC'],
        'aircon_heater': ['エアコン暖房', 'air conditioning heater'],
        'internet_wifi': ['WiFi', 'インターネット', 'internet', 'ネット'],
        'cable': ['ケーブルTV', 'cable', 'CATV'],
        'bs': ['BS', 'BS放送', 'satellite'],
        
        # Kitchen
        'system_kitchen': ['システムキッチン', 'system kitchen'],
        'counter_kitchen': ['カウンターキッチン', 'counter kitchen'],
        'full_kitchen': ['フルキッチン', 'full kitchen'],
        'induction_cooker': ['IHクッキング', 'induction', 'IH'],
        'gas': ['ガス', 'gas'],
        'microwave': ['電子レンジ', 'microwave'],
        'oven': ['オーブン', 'oven'],
        'dishwasher': ['食洗機', 'dishwasher', '食器洗い'],
        'refrigerator': ['冷蔵庫', 'refrigerator', '冷蔵'],
        'refrigerator_freezer': ['冷凍冷蔵庫', 'freezer'],
        
        # Bathroom
        'bath': ['バス', 'bath', '浴室'],
        'separate_toilet': ['独立洗面台', 'separate toilet', '独立'],
        'unit_bath': ['ユニットバス', 'unit bath'],
        'auto_fill_bath': ['自動給湯', 'auto fill'],
        'shower': ['シャワー', 'shower'],
        'japanese_toilet': ['和式トイレ', 'japanese toilet'],
        'western_toilet': ['洋式トイレ', 'western toilet'],
        'washlet': ['ウォシュレット', 'washlet'],
        
        # Flooring & Interior
        'flooring': ['フローリング', 'flooring', 'フロア'],
        'tatami': ['畳', 'tatami'],
        'carpet': ['カーペット', 'carpet'],
        'underfloor_heating': ['床暖房', 'underfloor heating'],
        
        # Storage & Space
        'storage': ['収納', 'storage', 'クローゼット'],
        'loft': ['ロフト', 'loft'],
        'balcony': ['バルコニー', 'balcony'],
        'veranda': ['ベランダ', 'veranda'],
        'roof_balcony': ['ルーフバルコニー', 'roof balcony'],
        'yard': ['庭', 'yard', 'ガーデン'],
        
        # Appliances
        'washing_machine': ['洗濯機', 'washing machine'],
        'washer_dryer': ['洗濯乾燥機', 'washer dryer'],
        'furnished': ['家具付き', 'furnished', '家具'],
        'all_electric': ['オール電化', 'all electric'],
        
        # Special features
        'pets': ['ペット', 'pet', 'ペット可'],
        'female_only': ['女性限定', 'female only', '女性専用'],
        'student_friendly': ['学生可', 'student', '学生'],
        'soho': ['SOHO', 'soho', '事務所可'],
        'newly_built': ['新築', 'newly built', '新築物件']
    }