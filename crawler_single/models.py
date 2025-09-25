from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime


class PropertyImage(BaseModel):
    """
    Model cho hình ảnh bất động sản
    """
    category: Optional[str] = Field(None, description="Danh mục hình ảnh (ví dụ: exterior, interior, kitchen, bathroom)")
    url: Optional[str] = Field(None, description="URL của hình ảnh")
    
    class Config:
        schema_extra = {
            "example": {
                "category": "exterior",
                "url": "https://example.com/property_image.jpg"
            }
        }


class PropertyModel(BaseModel):
    """
    Pydantic model cho dữ liệu bất động sản
    """
    
    # Thông tin cơ bản
    link: Optional[str] = Field(None, description="URL đến danh sách bất động sản")
    property_csv_id: Optional[str] = Field(None, description="Mã định danh duy nhất cho bất động sản ở định dạng CSV")
    
    # Địa chỉ
    postcode: Optional[str] = Field(None, description="Mã bưu điện của bất động sản")
    prefecture: Optional[str] = Field(None, description="Tỉnh nơi bất động sản tọa lạc")
    city: Optional[str] = Field(None, description="Thành phố nơi bất động sản tọa lạc")
    district: Optional[str] = Field(None, description="Quận hoặc phường của bất động sản")
    chome_banchi: Optional[str] = Field(None, description="Số khối và lô (hệ thống địa chỉ Nhật Bản)")
    
    # Thông tin tòa nhà
    building_type: Optional[str] = Field(None, description="Loại tòa nhà (ví dụ: chung cư, nhà riêng)")
    year: Optional[int] = Field(None, description="Năm xây dựng tòa nhà")
    
    # Tên tòa nhà đa ngôn ngữ
    building_name_en: Optional[str] = Field(None, description="Tên tòa nhà bằng tiếng Anh")
    building_name_ja: Optional[str] = Field(None, description="Tên tòa nhà bằng tiếng Nhật")
    
    # Mô tả tòa nhà đa ngôn ngữ
    building_description_en: Optional[str] = Field(None, description="Mô tả tòa nhà bằng tiếng Anh")
    building_description_ja: Optional[str] = Field(None, description="Mô tả tòa nhà bằng tiếng Nhật")
    
    # Địa danh gần đó đa ngôn ngữ
    building_landmarks_en: Optional[str] = Field(None, description="Các địa danh gần đó bằng tiếng Anh")
    building_landmarks_ja: Optional[str] = Field(None, description="Các địa danh gần đó bằng tiếng Nhật")
    
    # Thông tin ga tàu 1
    station_name_1: Optional[str] = Field(None, description="Tên ga tàu gần nhất (thứ 1)")
    train_line_name_1: Optional[str] = Field(None, description="Tên tuyến tàu cho ga 1")
    walk_1: Optional[int] = Field(None, description="Thời gian đi bộ đến ga 1 (phút)")
    bus_1: Optional[int] = Field(None, description="Thời gian đi xe buýt đến ga 1 (phút)")
    car_1: Optional[int] = Field(None, description="Thời gian đi ô tô đến ga 1 (phút)")
    cycle_1: Optional[int] = Field(None, description="Thời gian đi xe đạp đến ga 1 (phút)")
    
    # Thông tin ga tàu 2
    station_name_2: Optional[str] = Field(None, description="Tên ga tàu gần thứ hai")
    train_line_name_2: Optional[str] = Field(None, description="Tên tuyến tàu cho ga 2")
    walk_2: Optional[int] = Field(None, description="Thời gian đi bộ đến ga 2 (phút)")
    bus_2: Optional[int] = Field(None, description="Thời gian đi xe buýt đến ga 2 (phút)")
    car_2: Optional[int] = Field(None, description="Thời gian đi ô tô đến ga 2 (phút)")
    cycle_2: Optional[int] = Field(None, description="Thời gian đi xe đạp đến ga 2 (phút)")
    
    # Thông tin ga tàu 3
    station_name_3: Optional[str] = Field(None, description="Tên ga tàu gần thứ ba")
    train_line_name_3: Optional[str] = Field(None, description="Tên tuyến tàu cho ga 3")
    walk_3: Optional[int] = Field(None, description="Thời gian đi bộ đến ga 3 (phút)")
    bus_3: Optional[int] = Field(None, description="Thời gian đi xe buýt đến ga 3 (phút)")
    car_3: Optional[int] = Field(None, description="Thời gian đi ô tô đến ga 3 (phút)")
    cycle_3: Optional[int] = Field(None, description="Thời gian đi xe đạp đến ga 3 (phút)")
    
    # Thông tin ga tàu 4
    station_name_4: Optional[str] = Field(None, description="Tên ga tàu gần thứ tư")
    train_line_name_4: Optional[str] = Field(None, description="Tên tuyến tàu cho ga 4")
    walk_4: Optional[int] = Field(None, description="Thời gian đi bộ đến ga 4 (phút)")
    bus_4: Optional[int] = Field(None, description="Thời gian đi xe buýt đến ga 4 (phút)")
    car_4: Optional[int] = Field(None, description="Thời gian đi ô tô đến ga 4 (phút)")
    cycle_4: Optional[int] = Field(None, description="Thời gian đi xe đạp đến ga 4 (phút)")
    
    # Thông tin ga tàu 5
    station_name_5: Optional[str] = Field(None, description="Tên ga tàu gần thứ năm")
    train_line_name_5: Optional[str] = Field(None, description="Tên tuyến tàu cho ga 5")
    walk_5: Optional[int] = Field(None, description="Thời gian đi bộ đến ga 5 (phút)")
    bus_5: Optional[int] = Field(None, description="Thời gian đi xe buýt đến ga 5 (phút)")
    car_5: Optional[int] = Field(None, description="Thời gian đi ô tô đến ga 5 (phút)")
    cycle_5: Optional[int] = Field(None, description="Thời gian đi xe đạp đến ga 5 (phút)")
    
    # Tọa độ địa lý
    map_lat: Optional[float] = Field(None, description="Vĩ độ của vị trí bất động sản")
    map_lng: Optional[float] = Field(None, description="Kinh độ của vị trí bất động sản")
    
    # Thông tin cấu trúc tòa nhà
    num_units: Optional[int] = Field(None, description="Số căn hộ trong tòa nhà")
    floors: Optional[int] = Field(None, description="Số tầng của tòa nhà")
    basement_floors: Optional[int] = Field(None, description="Số tầng hầm")
    
    # Thông tin đậu xe
    parking: Optional[Literal['Y', 'N']] = Field(None, description="Có chỗ đậu xe không? ('Y' hoặc 'N')")
    parking_cost: Optional[int] = Field(None, description="Chi phí đậu xe (hàng tháng)")
    bicycle_parking: Optional[Literal['Y', 'N']] = Field(None, description="Có chỗ đậu xe đạp không? ('Y' hoặc 'N')")
    motorcycle_parking: Optional[Literal['Y', 'N']] = Field(None, description="Có chỗ đậu xe máy không? ('Y' hoặc 'N')")
    
    # Thông tin cấu trúc và phong cách
    structure: Optional[str] = Field(None, description="Loại cấu trúc tòa nhà (ví dụ: thép, gỗ, khác)")
    building_notes: Optional[str] = Field(None, description="Ghi chú bổ sung về tòa nhà")
    building_style: Optional[str] = Field(None, description="Phong cách tòa nhà (ví dụ: bình thường, sang trọng)")
    
    # Tiện ích tòa nhà
    autolock: Optional[Literal['Y', 'N']] = Field(None, description="Có hệ thống khóa tự động không? ('Y' hoặc 'N')")
    credit_card: Optional[Literal['Y', 'N']] = Field(None, description="Có chấp nhận thẻ tín dụng không? ('Y' hoặc 'N')")
    concierge: Optional[Literal['Y', 'N']] = Field(None, description="Có dịch vụ lễ tân không? ('Y' hoặc 'N')")
    delivery_box: Optional[Literal['Y', 'N']] = Field(None, description="Có hộp giao hàng không? ('Y' hoặc 'N')")
    elevator: Optional[Literal['Y', 'N']] = Field(None, description="Có thang máy không? ('Y' hoặc 'N')")
    gym: Optional[Literal['Y', 'N']] = Field(None, description="Có phòng tập thể dục không? ('Y' hoặc 'N')")
    newly_built: Optional[Literal['Y', 'N']] = Field(None, description="Tòa nhà có mới xây không? ('Y' hoặc 'N')")
    pets: Optional[Literal['Y', 'N']] = Field(None, description="Có cho phép nuôi thú cưng không? ('Y' hoặc 'N')")
    swimming_pool: Optional[Literal['Y', 'N']] = Field(None, description="Có hồ bơi không? ('Y' hoặc 'N')")
    ur: Optional[Literal['Y', 'N']] = Field(None, description="Có phải là bất động sản Urban Renaissance không? ('Y' hoặc 'N')")
    
    # Thông tin căn hộ
    room_type: Optional[str] = Field(None, description="Loại phòng/mặt bằng (ví dụ: 1K, 2DK)")
    size: Optional[float] = Field(None, description="Diện tích phòng (mét vuông)")
    unit_no: Optional[int] = Field(None, description="Số căn hộ")
    ad_type: Optional[str] = Field(None, description="Loại quảng cáo (ví dụ: đại lý, chủ sở hữu)")
    available_from: Optional[str] = Field(None, description="Ngày bất động sản có sẵn")
    
    # Mô tả bất động sản đa ngôn ngữ
    property_description_en: Optional[str] = Field(None, description="Mô tả bất động sản bằng tiếng Anh")
    property_description_ja: Optional[str] = Field(None, description="Mô tả bất động sản bằng tiếng Nhật")
    
    # Chi phí khác đa ngôn ngữ
    property_other_expenses_en: Optional[str] = Field(None, description="Chi phí khác (tiếng Anh)")
    property_other_expenses_ja: Optional[str] = Field(None, description="Chi phí khác (tiếng Nhật)")
    
    # Loại nổi bật
    featured_a: Optional[Literal['Y', 'N']] = Field(None, description="Có phải là loại nổi bật A không? ('Y' hoặc 'N')")
    featured_b: Optional[Literal['Y', 'N']] = Field(None, description="Có phải là loại nổi bật B không? ('Y' hoặc 'N')")
    featured_c: Optional[Literal['Y', 'N']] = Field(None, description="Có phải là loại nổi bật C không? ('Y' hoặc 'N')")
    
    # Thông tin tầng và giá thuê
    floor_no: Optional[int] = Field(None, description="Số tầng của căn hộ")
    monthly_rent: Optional[int] = Field(None, description="Số tiền thuê hàng tháng")
    monthly_maintenance: Optional[int] = Field(None, description="Phí bảo trì hàng tháng")
    
    # Các khoản phí (theo tháng và số tiền)
    months_deposit: Optional[int] = Field(None, description="Tiền đặt cọc yêu cầu (tháng)")
    numeric_deposit: Optional[int] = Field(None, description="Tiền đặt cọc yêu cầu (số tiền)")
    months_key: Optional[int] = Field(None, description="Tiền chìa khóa yêu cầu (tháng)")
    numeric_key: Optional[int] = Field(None, description="Tiền chìa khóa yêu cầu (số tiền)")
    months_guarantor: Optional[int] = Field(None, description="Phí người bảo lãnh yêu cầu (tháng)")
    numeric_guarantor: Optional[int] = Field(None, description="Phí người bảo lãnh yêu cầu (số tiền)")
    months_agency: Optional[int] = Field(None, description="Phí đại lý yêu cầu (tháng)")
    numeric_agency: Optional[int] = Field(None, description="Phí đại lý yêu cầu (số tiền)")
    months_renewal: Optional[int] = Field(None, description="Phí gia hạn yêu cầu (tháng)")
    numeric_renewal: Optional[int] = Field(None, description="Phí gia hạn yêu cầu (số tiền)")
    months_deposit_amortization: Optional[int] = Field(None, description="Khấu hao tiền đặt cọc (tháng)")
    numeric_deposit_amortization: Optional[int] = Field(None, description="Khấu hao tiền đặt cọc (số tiền)")
    months_security_deposit: Optional[int] = Field(None, description="Tiền đặt cọc bảo đảm yêu cầu (tháng)")
    numeric_security_deposit: Optional[int] = Field(None, description="Tiền đặt cọc bảo đảm yêu cầu (số tiền)")
    
    # Các phí khác
    lock_exchange: Optional[int] = Field(None, description="Phí thay khóa")
    fire_insurance: Optional[int] = Field(None, description="Phí bảo hiểm cháy nổ")
    other_initial_fees: Optional[int] = Field(None, description="Các phí ban đầu khác")
    other_subscription_fees: Optional[int] = Field(None, description="Các phí đăng ký khác")
    
    # Thông tin bảo lãnh
    no_guarantor: Optional[Literal['Y', 'N']] = Field(None, description="Có yêu cầu không cần người bảo lãnh không? ('Y' hoặc 'N')")
    guarantor_agency: Optional[str] = Field(None, description="Yêu cầu đại lý bảo lãnh")
    guarantor_agency_name: Optional[str] = Field(None, description="Tên đại lý bảo lãnh")
    numeric_guarantor_max: Optional[int] = Field(None, description="Phí người bảo lãnh tối đa (số tiền)")
    
    # Thông tin thuê
    rent_negotiable: Optional[Literal['Y', 'N']] = Field(None, description="Tiền thuê có thể thương lượng không? ('Y' hoặc 'N')")
    renewal_new_rent: Optional[Literal['Y', 'N']] = Field(None, description="Có áp dụng tiền thuê mới khi gia hạn không? ('Y' hoặc 'N')")
    lease_date: Optional[str] = Field(None, description="Ngày bắt đầu hợp đồng thuê")
    lease_months: Optional[int] = Field(None, description="Thời hạn thuê tính bằng tháng")
    lease_type: Optional[str] = Field(None, description="Loại hợp đồng thuê (ví dụ: thường, ngắn hạn)")
    short_term_ok: Optional[Literal['Y', 'N']] = Field(None, description="Có cho phép thuê ngắn hạn không? ('Y' hoặc 'N')")
    
    # Thông tin ban công và ghi chú
    balcony_size: Optional[float] = Field(None, description="Diện tích ban công (mét vuông)")
    property_notes: Optional[str] = Field(None, description="Ghi chú bổ sung về bất động sản")
    discount: Optional[int] = Field(None, description="Số tiền giảm giá")
    
    # Hướng căn hộ
    facing_north: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng bắc không? ('Y' hoặc 'N')")
    facing_northeast: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng đông bắc không? ('Y' hoặc 'N')")
    facing_east: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng đông không? ('Y' hoặc 'N')")
    facing_southeast: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng đông nam không? ('Y' hoặc 'N')")
    facing_south: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng nam không? ('Y' hoặc 'N')")
    facing_southwest: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng tây nam không? ('Y' hoặc 'N')")
    facing_west: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng tây không? ('Y' hoặc 'N')")
    facing_northwest: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có hướng tây bắc không? ('Y' hoặc 'N')")
    
    # Tiện nghi căn hộ
    aircon: Optional[Literal['Y', 'N']] = Field(None, description="Có điều hòa không khí không? ('Y' hoặc 'N')")
    aircon_heater: Optional[Literal['Y', 'N']] = Field(None, description="Có điều hòa với máy sưởi không? ('Y' hoặc 'N')")
    all_electric: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có toàn bộ điện không? ('Y' hoặc 'N')")
    auto_fill_bath: Optional[Literal['Y', 'N']] = Field(None, description="Có bồn tắm tự động đổ nước không? ('Y' hoặc 'N')")
    balcony: Optional[Literal['Y', 'N']] = Field(None, description="Có ban công không? ('Y' hoặc 'N')")
    bath: Optional[Literal['Y', 'N']] = Field(None, description="Có bồn tắm không? ('Y' hoặc 'N')")
    bath_water_heater: Optional[Literal['Y', 'N']] = Field(None, description="Có máy nước nóng cho bồn tắm không? ('Y' hoặc 'N')")
    blinds: Optional[Literal['Y', 'N']] = Field(None, description="Có rèm che không? ('Y' hoặc 'N')")
    bs: Optional[Literal['Y', 'N']] = Field(None, description="Có BS (vệ tinh phát sóng) không? ('Y' hoặc 'N')")
    cable: Optional[Literal['Y', 'N']] = Field(None, description="Có truyền hình cáp không? ('Y' hoặc 'N')")
    carpet: Optional[Literal['Y', 'N']] = Field(None, description="Có sàn thảm không? ('Y' hoặc 'N')")
    cleaning_service: Optional[Literal['Y', 'N']] = Field(None, description="Có dịch vụ dọn dẹp không? ('Y' hoặc 'N')")
    counter_kitchen: Optional[Literal['Y', 'N']] = Field(None, description="Có bếp quầy bar không? ('Y' hoặc 'N')")
    dishwasher: Optional[Literal['Y', 'N']] = Field(None, description="Có máy rửa bát không? ('Y' hoặc 'N')")
    drapes: Optional[Literal['Y', 'N']] = Field(None, description="Có rèm cửa không? ('Y' hoặc 'N')")
    female_only: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ chỉ dành cho nữ không? ('Y' hoặc 'N')")
    fireplace: Optional[Literal['Y', 'N']] = Field(None, description="Có lò sưởi không? ('Y' hoặc 'N')")
    flooring: Optional[Literal['Y', 'N']] = Field(None, description="Có sàn lát không? ('Y' hoặc 'N')")
    full_kitchen: Optional[Literal['Y', 'N']] = Field(None, description="Có bếp đầy đủ không? ('Y' hoặc 'N')")
    furnished: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có nội thất không? ('Y' hoặc 'N')")
    gas: Optional[Literal['Y', 'N']] = Field(None, description="Có gas không? ('Y' hoặc 'N')")
    induction_cooker: Optional[Literal['Y', 'N']] = Field(None, description="Có bếp từ không? ('Y' hoặc 'N')")
    internet_broadband: Optional[Literal['Y', 'N']] = Field(None, description="Có internet băng thông rộng không? ('Y' hoặc 'N')")
    internet_wifi: Optional[Literal['Y', 'N']] = Field(None, description="Có WiFi không? ('Y' hoặc 'N')")
    japanese_toilet: Optional[Literal['Y', 'N']] = Field(None, description="Có toilet kiểu Nhật không? ('Y' hoặc 'N')")
    linen: Optional[Literal['Y', 'N']] = Field(None, description="Có ga trải giường không? ('Y' hoặc 'N')")
    loft: Optional[Literal['Y', 'N']] = Field(None, description="Có gác lửng không? ('Y' hoặc 'N')")
    microwave: Optional[Literal['Y', 'N']] = Field(None, description="Có lò vi sóng không? ('Y' hoặc 'N')")
    oven: Optional[Literal['Y', 'N']] = Field(None, description="Có lò nướng không? ('Y' hoặc 'N')")
    phoneline: Optional[Literal['Y', 'N']] = Field(None, description="Có đường dây điện thoại không? ('Y' hoặc 'N')")
    range: Optional[Literal['Y', 'N']] = Field(None, description="Có bếp gas không? ('Y' hoặc 'N')")
    refrigerator: Optional[Literal['Y', 'N']] = Field(None, description="Có tủ lạnh không? ('Y' hoặc 'N')")
    refrigerator_freezer: Optional[Literal['Y', 'N']] = Field(None, description="Có tủ lạnh với ngăn đông không? ('Y' hoặc 'N')")
    roof_balcony: Optional[Literal['Y', 'N']] = Field(None, description="Có ban công trên mái không? ('Y' hoặc 'N')")
    separate_toilet: Optional[Literal['Y', 'N']] = Field(None, description="Có toilet riêng biệt không? ('Y' hoặc 'N')")
    shower: Optional[Literal['Y', 'N']] = Field(None, description="Có vòi sen không? ('Y' hoặc 'N')")
    soho: Optional[Literal['Y', 'N']] = Field(None, description="Có cho phép SOHO (văn phòng nhỏ/văn phòng tại nhà) không? ('Y' hoặc 'N')")
    storage: Optional[Literal['Y', 'N']] = Field(None, description="Có kho chứa không? ('Y' hoặc 'N')")
    student_friendly: Optional[Literal['Y', 'N']] = Field(None, description="Căn hộ có thân thiện với sinh viên không? ('Y' hoặc 'N')")
    system_kitchen: Optional[Literal['Y', 'N']] = Field(None, description="Có bếp hệ thống không? ('Y' hoặc 'N')")
    tatami: Optional[Literal['Y', 'N']] = Field(None, description="Có sàn tatami không? ('Y' hoặc 'N')")
    underfloor_heating: Optional[Literal['Y', 'N']] = Field(None, description="Có sưởi sàn không? ('Y' hoặc 'N')")
    unit_bath: Optional[Literal['Y', 'N']] = Field(None, description="Có phòng tắm đơn vị không? ('Y' hoặc 'N')")
    utensils_cutlery: Optional[Literal['Y', 'N']] = Field(None, description="Có đồ dùng và dao kéo không? ('Y' hoặc 'N')")
    veranda: Optional[Literal['Y', 'N']] = Field(None, description="Có hiên nhà không? ('Y' hoặc 'N')")
    washer_dryer: Optional[Literal['Y', 'N']] = Field(None, description="Có máy giặt/sấy không? ('Y' hoặc 'N')")
    washing_machine: Optional[Literal['Y', 'N']] = Field(None, description="Có máy giặt không? ('Y' hoặc 'N')")
    washlet: Optional[Literal['Y', 'N']] = Field(None, description="Có washlet (toilet rửa) không? ('Y' hoặc 'N')")
    western_toilet: Optional[Literal['Y', 'N']] = Field(None, description="Có toilet kiểu Tây không? ('Y' hoặc 'N')")
    yard: Optional[Literal['Y', 'N']] = Field(None, description="Có sân không? ('Y' hoặc 'N')")
    
    # Media links
    youtube: Optional[str] = Field(None, description="Liên kết video YouTube cho bất động sản")
    vr_link: Optional[str] = Field(None, description="Liên kết tour thực tế ảo cho bất động sản")
    
    # Hình ảnh (danh sách linh hoạt)
    images: Optional[List[PropertyImage]] = Field(default_factory=list, description="Danh sách hình ảnh của bất động sản")
    
    # Ngày tạo
    create_date: Optional[str] = Field(None, description="Ngày tạo bất động sản (timestamp)")
    
    class Config:
        """Cấu hình cho Pydantic model"""
        # Cho phép sử dụng enum values
        use_enum_values = True
        # Validate assignment
        validate_assignment = True
        # Cho phép population by name
        allow_population_by_field_name = True
        # Schema extra để tạo example
        schema_extra = {
            "example": {
                "property_csv_id": "PROP001",
                "prefecture": "Tokyo",
                "city": "Shibuya",
                "district": "Shibuya",
                "building_type": "Apartment",
                "year": 2020,
                "building_name_en": "Tokyo Heights",
                "room_type": "1K",
                "size": 25.5,
                "monthly_rent": 120000,
                "parking": "Y",
                "elevator": "Y",
                "aircon": "Y",
                "internet_wifi": "Y",
                "map_lat": 35.6762,
                "map_lng": 139.6503,
                "walk_1": 5,
                "floor_no": 3,
                "floors": 10,
                "num_units": 50,
                "parking_cost": 15000,
                "balcony_size": 8.5,
                "lease_months": 24,
                "images": [
                    {"category": "exterior", "url": "https://example.com/exterior1.jpg"},
                    {"category": "interior", "url": "https://example.com/interior1.jpg"},
                    {"category": "kitchen", "url": "https://example.com/kitchen1.jpg"}
                ]
            }
        }

class AmenityKeywords:
    """Keywords cho việc detect amenities"""
    
    AMENITY_KEYWORDS = {
        # Building amenities
        'elevator': ['エレベーター', 'elevator', 'EV'],
        'autolock': ['オートロック', 'auto lock', 'autoloc'],
        'delivery_box': ['宅配ボックス', 'delivery box', '宅配BOX', '宅配ロッカー'],
        'concierge': ['コンシェルジュ', 'concierge', 'フロント'],
        'gym': ['ジム', 'gym', 'フィットネス'],
        'swimming_pool': ['プール', 'pool', 'swimming'],
        
        # Parking - with more specific keywords
        'parking': ['駐車場有', '駐車場', 'parking', '駐車可', '車庫'],
        'bicycle_parking': ['駐輪場', 'bicycle parking', '自転車置場', '自転車'],
        'motorcycle_parking': ['バイク置場', 'motorcycle', 'バイク駐車', 'バイク'],
        
        # Unit amenities
        'aircon': ['エアコン', 'air conditioning', 'aircon', 'AC', '冷暖房'],
        'aircon_heater': ['エアコン暖房', 'air conditioning heater'],
        'internet_wifi': ['WiFi', 'インターネット', 'internet', 'ネット', 'ブロードバンド'],
        'cable': ['ケーブルTV', 'cable', 'CATV'],
        'bs': ['BS', 'BS放送', 'satellite', 'BS有'],
        
        # Kitchen
        'system_kitchen': ['システムキッチン', 'system kitchen'],
        'counter_kitchen': ['カウンターキッチン', 'counter kitchen'],
        'full_kitchen': ['フルキッチン', 'full kitchen'],
        'induction_cooker': ['IHクッキング', 'induction', 'IH'],
        'gas': ['ガス', 'gas', 'ガスコンロ'],
        'microwave': ['電子レンジ', 'microwave'],
        'oven': ['オーブン', 'oven'],
        'dishwasher': ['食洗機', 'dishwasher', '食器洗い'],
        'refrigerator': ['冷蔵庫', 'refrigerator', '冷蔵'],
        'refrigerator_freezer': ['冷凍冷蔵庫', 'freezer'],
        
        # Bathroom - enhanced with more Japanese terms
        'bath': ['バス', 'bath', '浴室', 'バス有', '浴槽'],
        'separate_toilet': ['独立洗面台', 'separate toilet', '独立', 'バストイレ別'],
        'unit_bath': ['ユニットバス', 'unit bath', 'バストイレ'],
        'auto_fill_bath': ['自動給湯', 'auto fill', '給湯追い焚き有', '追い焚き'],
        'shower': ['シャワー', 'shower'],
        'japanese_toilet': ['和式トイレ', 'japanese toilet'],
        'western_toilet': ['洋式トイレ', 'western toilet'],
        'washlet': ['ウォシュレット', 'washlet'],
        
        # Flooring & Interior
        'flooring': ['フローリング', 'flooring', 'フロア'],
        'tatami': ['畳', 'tatami'],
        'carpet': ['カーペット', 'carpet'],
        'underfloor_heating': ['床暖房', 'underfloor heating'],
        
        # Storage & Space - enhanced
        'storage': ['収納', 'storage', 'クローゼット', '室内洗濯機置場'],
        'loft': ['ロフト', 'loft'],
        'balcony': ['バルコニー', 'balcony'],
        'veranda': ['ベランダ', 'veranda'],
        'roof_balcony': ['ルーフバルコニー', 'roof balcony'],
        'yard': ['庭', 'yard', 'ガーデン'],
        
        # Appliances - enhanced
        'washing_machine': ['洗濯機', 'washing machine', '室内洗濯機置場'],
        'washer_dryer': ['洗濯乾燥機', 'washer dryer', '浴室乾燥機'],
        'furnished': ['家具付き', 'furnished', '家具'],
        'all_electric': ['オール電化', 'all electric'],
        
        # Special features - enhanced
        'pets': ['ペット', 'pet', 'ペット可', 'ペット相談'],
        'female_only': ['女性限定', 'female only', '女性専用'],
        'student_friendly': ['学生可', 'student', '学生'],
        'soho': ['SOHO', 'soho', '事務所可', 'ピアノ可'],
        'newly_built': ['新築', 'newly built', '新築物件']
    }


# Thêm class method vào PropertyModel để tạo empty data
def get_empty_property_data(url: str) -> Dict[str, Any]:
    """
    Tạo cấu trúc dữ liệu property rỗng với tất cả fields từ PropertyModel
    """
    # Tạo một instance rỗng của PropertyModel
    empty_model = PropertyModel()
    
    # Convert sang dict và set các giá trị cần thiết
    data = empty_model.dict()
    data['link'] = url
    
    return data