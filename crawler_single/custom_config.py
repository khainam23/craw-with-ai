"""
Custom Configuration - Setup your custom rules and hooks here
"""
import re
from typing import Dict, Any
from .custom_rules import CustomExtractor, RuleBuilder, ExtractionRule


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
        
        # Keep _html for image extraction, it will be cleaned up later
        return data
    
    # Pre-hook to pass HTML to post-hook
    def pass_html(html: str, data: Dict[str, Any]) -> tuple:
        # Remove section tags with class containing "--related"
        html = re.sub(r'<section[^>]*class="[^"]*--related[^"]*"[^>]*>.*?</section>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove the specific Japanese text section about related properties
        html = re.sub(r'この部屋をチェックした人は、こんな部屋もチェックしています。.*?(?=<footer|$)', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        data['_html'] = html
        return html, data
    
    extractor.add_pre_hook(pass_html)
    extractor.add_post_hook(convert_coordinates)
    
    return extractor