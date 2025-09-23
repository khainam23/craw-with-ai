from pyproj import CRS, Transformer

def xy_to_latlon_tokyo(x, y, zone=9):
    """
    Chuyển đổi từ tọa độ phẳng XY (Japan Plane Rectangular CS dựa trên Tokyo Datum) về lat/lon (WGS84).
    :param x: X coordinate (m)
    :param y: Y coordinate (m)
    :param zone: Zone number (1-19)
    :return: (lat, lon) in degrees
    """
    # Định nghĩa hệ tọa độ phẳng Nhật Bản dựa trên Tokyo Datum
    epsg_code = 30160 + zone  # Zone 9 -> EPSG:30169 (Tokyo / Japan Plane Rectangular CS IX)
    crs_xy = CRS.from_epsg(epsg_code)
    
    # Hệ tọa độ chuẩn WGS84
    crs_wgs84 = CRS.from_epsg(4326)
    
    # Tạo transformer
    transformer = Transformer.from_crs(crs_xy, crs_wgs84, always_xy=True)
    
    # Chuyển đổi
    lon, lat = transformer.transform(x, y)
    return lat - 1.291213 , lon - 5.82497 # Sai số trên lệch, tính dựa vào thống kê trung bình nhiều điểm