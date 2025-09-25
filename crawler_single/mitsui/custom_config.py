"""
Custom Configuration - Setup your custom rules and hooks here
"""
import re
import requests
from typing import Dict, Any
from ..custom_rules import CustomExtractor

def setup_custom_extractor() -> CustomExtractor:
    """
    Setup custom extractor - Add your rules and hooks here
    """
    extractor = CustomExtractor()
    
    # Convert X,Y coordinates to lat/lng
    def convert_coordinates(data: Dict[str, Any]) -> Dict[str, Any]:
        html = data.get('_html', '')  # We'll pass HTML through data
        
        # Extract MAP_X
        x_match = re.search(r'name="[^"]*MAP_X"[^>]*value="([^"]*)"', html, re.IGNORECASE)
        # Extract MAP_Y  
        y_match = re.search(r'name="[^"]*MAP_Y"[^>]*value="([^"]*)"', html, re.IGNORECASE)
        
        if x_match and y_match:
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from utils.convert_gis import xy_to_latlon_tokyo
                
                x = float(x_match.group(1))
                y = float(y_match.group(1))
                
                lat, lon = xy_to_latlon_tokyo(x, y, zone=9)
                
                data['map_lat'] = str(lat)
                data['map_lng'] = str(lon)
                
                print(f"🗺️ Converted: X={x}, Y={y} → Lat={lat:.6f}, Lng={lon:.6f}")
                
            except Exception as e:
                print(f"❌ Coordinate conversion error: {e}")
        
        # Keep _html for image extraction from cleaned HTML, will be cleaned up after processing
        return data
    
    # Pre-hook to pass HTML to post-hook
    def pass_html(html: str, data: Dict[str, Any]) -> tuple:
        # Remove section tags with class containing "--related"
        html = re.sub(r'<section[^>]*class="[^"]*--related[^"]*"[^>]*>.*?</section>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove the specific Japanese text section about related properties
        html = re.sub(r'この部屋をチェックした人は、こんな部屋もチェックしています。.*?(?=<footer|$)', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        data['_html'] = html
        return html, data
    
    def extract_image(data: Dict[str, Any]) -> Dict[str, Any]:
        html = data.get('_html', '')
        if not html:
            return data

        used_urls = set()
        used_name = set()
        images_list = []

        def add_image(img_url: str, category: str):
            """Thêm ảnh vào images list"""
            if img_url not in used_urls and img_url.split('/')[-1] not in used_name and len(images_list) < 16:
                image_data = {
                    'url': img_url,
                    'category': category
                }
                images_list.append(image_data)
                used_urls.add(img_url)
                used_name.add(img_url.split('/')[-1])

        def extract_js_var(var_name: str) -> str:
            """Tìm giá trị biến JS trong source HTML"""
            match = re.search(rf'{var_name}\s*=\s*["\']([^"\']+)["\']', html)
            return match.group(1) if match else None

        try:
            # 1. Floor plan
            firstfloor_url = extract_js_var("RF_firstfloorplan_photo")
            if firstfloor_url and firstfloor_url != "null":
                add_image(firstfloor_url, "floorplan")

            # 2. Gallery
            gallery_url = extract_js_var("RF_gallery_url")
            if gallery_url and gallery_url != "null":
                print(f"🖼️ Fetching gallery from: {gallery_url}")
                response = requests.get(gallery_url, timeout=10)
                if response.status_code == 200:
                    gallery_data = response.json()
                    for item in gallery_data:
                        room_no = item.get("ROOM_NO", 0)
                        filename = item.get("filename", "")
                        if room_no != 99999 and filename:
                            add_image(filename, "interior")
                else:
                    print(f"❌ Failed to fetch gallery: HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Extraction error: {e}")

        # Gán images list vào data
        if images_list:
            data['images'] = images_list
            print(f"🎯 Total images extracted: {len(images_list)}")
        
        return data
    
    # Set default amenities to Y
    def set_default_amenities(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set specific amenities to Y by default
        """
        default_amenities = {
            'credit_card': 'Y',         # Credit Card Accepted
            'no_guarantor': 'Y',        # No Guarantor
            'aircon': 'Y',              # Aircon
            'aircon_heater': 'Y',       # Aircon Heater
            'bs': 'Y',                  # Broadcast Satellite TV
            'cable': 'Y',               # Cable
            'internet_broadband': 'Y',  # Broadband
            'internet_wifi': 'Y',       # Internet WiFi
            'phoneline': 'Y',           # Phoneline
            'flooring': 'Y',            # Flooring
            'system_kitchen': 'Y',      # System Kitchen
            'bath': 'Y',                # Bath
            'shower': 'Y',              # Shower
            'unit_bath': 'Y',           # Unit Bath
            'western_toilet': 'Y',      # Western Toilet
            'fire_insurance': 20000,    # Insurance Fee
        }
    
        
        # Set all default amenities to Y
        for field_name, value in default_amenities.items():
            data[field_name] = value
        
        return data
    
    # Process pricing from めやす賃料 field
    def process_pricing(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract めやす賃料 from HTML using regex and calculate monthly_rent and monthly_maintenance.
        """
        html = data.get('_html', '')
        if not html:
            return data

        def extract_price_from_html(field_name: str) -> str:
            """
            Tìm giá trị trong <dd> ngay sau <dt>field_name</dt>.
            """
            pattern = rf"<dt[^>]*>{field_name}</dt>\s*<dd[^>]*>(.*?)</dd>"
            match = re.search(pattern, html, re.DOTALL)
            return match.group(1).strip() if match else ""

        try:
            total_monthly_raw = extract_price_from_html("めやす賃料")
            print(f"💸 Processing pricing: めやす賃料={total_monthly_raw}")

            if total_monthly_raw:
                numeric_match = re.search(r"([\d,]+)", total_monthly_raw)
                if numeric_match:
                    total_monthly = int(numeric_match.group(1).replace(",", ""))

                    # Tính toán
                    numeric_guarantor = total_monthly * 50 // 100
                    numeric_guarantor_max = total_monthly * 80 // 100

                    # Ghi vào data
                    data.update({
                        "total_monthly": total_monthly,
                        "numeric_guarantor": numeric_guarantor,
                        "numeric_guarantor_max": numeric_guarantor_max,
                    })

                    print(f"💰 Processed pricing:")
                    print(f"   total_monthly = {total_monthly:,}円")
                    print(f"   numeric_guarantor = {numeric_guarantor:,}円 (50%)")
                    print(f"   numeric_guarantor_max = {numeric_guarantor_max:,}円 (80%)")
                else:
                    print(f"⚠️ Could not extract numeric value from: {total_monthly_raw}")

        except Exception as e:
            print(f"❌ Error processing pricing: {e}")

        return data
    
    # Cleanup hook to remove temporary fields
    def cleanup_temp_fields(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove temporary fields that shouldn't be in final JSON
        """
        # Remove _html field used for processing
        if '_html' in data:
            del data['_html']
            print("🧹 Cleaned up temporary _html field")
        
        return data
    
    extractor.add_pre_hook(pass_html)
    extractor.add_post_hook(convert_coordinates)
    extractor.add_post_hook(set_default_amenities)
    extractor.add_post_hook(process_pricing)
    extractor.add_post_hook(extract_image)
    extractor.add_post_hook(cleanup_temp_fields)
    
    return extractor