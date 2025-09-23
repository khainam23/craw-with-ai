from typing import Dict, Any
from .extractors import (
    AddressParser,
    StationParser,
    PropertyDetailsParser
)


class MarkdownParser:
    """Refactored Markdown parser with separated concerns"""
    
    def __init__(self):
        # Initialize all parsers
        self.address_parser = AddressParser()
        self.station_parser = StationParser()
        self.property_parser = PropertyDetailsParser()
    
    def extract_from_markdown(self, markdown: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract additional data từ markdown content using specialized parsers
        """
        if not markdown:
            return data
        
        lines = markdown.split('\n')
        station_count = 1
        
        for line in lines:
            line = line.strip()
            
            # Extract address components
            data = self.address_parser.extract_address_info(line, data)
            
            # Extract station information
            station_count = self.station_parser.extract_station_info(line, data, station_count)
            
            # Extract property details
            data = self.property_parser.extract_building_type(line, data)
            data = self.property_parser.extract_available_date(line, data)
            data = self.property_parser.extract_postcode(line, data)
            data = self.property_parser.extract_unit_number(line, data)
        
        return data