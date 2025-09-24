from typing import Dict, Any
from .extractors import (
    BasicPropertyExtractor,
    AmenityExtractor,
    PricingExtractor,
    BuildingInfoExtractor,
    LocationExtractor,
    DateExtractor
)

class HTMLParser:
    """Refactored HTML parser with separated concerns"""
    
    def __init__(self):
        # Initialize all extractors
        self.basic_extractor = BasicPropertyExtractor()
        self.amenity_extractor = AmenityExtractor()
        self.pricing_extractor = PricingExtractor()
        self.building_extractor = BuildingInfoExtractor()
        self.location_extractor = LocationExtractor()
        self.date_extractor = DateExtractor()
    
    def extract_from_html_patterns(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured data từ HTML patterns using specialized extractors
        """
        if not html:
            return data
        
        # Extract basic property information
        data = self.basic_extractor.extract_rent_patterns(html, data)
        data = self.basic_extractor.extract_size_patterns(html, data)
        data = self.basic_extractor.extract_floor_patterns(html, data)
        data = self.basic_extractor.extract_year_patterns(html, data)
        
        # Extract amenities
        data = self.amenity_extractor.extract_amenities(html, data)
        
        # Extract pricing information
        data = self.pricing_extractor.extract_pricing_info(html, data)
        
        # Extract building information
        data = self.building_extractor.extract_building_info(html, data)
        
        # Extract location information
        data = self.location_extractor.extract_coordinates(html, data)
        data = self.location_extractor.extract_address_from_html(html, data)
        
        # Extract date information
        data = self.date_extractor.extract_available_date_from_html(html, data)
        
        return data