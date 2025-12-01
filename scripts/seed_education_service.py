import asyncio
import random
from datetime import datetime

import httpx

# Configuration
API_URL = "http://localhost:8008/api/v1"
HEADERS = {"Content-Type": "application/json"}

# Vietnamese Data
SCHOOL_TYPES = ["Tiểu học", "Trung học cơ sở", "Trung học phổ thông", "Đại học", "Cao đẳng"]
DISTRICTS = [
    "Hải Châu", "Thanh Khê", "Sơn Trà", "Ngũ Hành Sơn", "Liên Chiểu", "Cẩm Lệ", "Hòa Vang"
]

SCHOOL_NAMES = [
    "Trần Phú", "Phan Châu Trinh", "Hoàng Hoa Thám", "Nguyễn Khuyến", "Lê Quý Đôn",
    "Thái Phiên", "Nguyễn Trãi", "Nguyễn Thượng Hiền", "Trần Đại Nghĩa", "Lương Thế Vinh",
    "Nguyễn Hiền", "Ông Ích Khiêm", "Phạm Phú Thứ", "Nguyễn Văn Cừ", "Hòa Vang",
    "Ngô Quyền", "Tôn Thất Tùng", "Hồ Nghinh", "Võ Thị Sáu", "Trưng Vương"
]

FACILITIES = [
    "Pin năng lượng mặt trời", "Hệ thống tái chế nước", "Vườn trường", 
    "Thùng rác phân loại", "Cảm biến không khí", "Đèn LED tiết kiệm điện",
    "Thư viện xanh", "Khu ủ phân hữu cơ", "Trạm sạc xe điện"
]

COURSES = [
    {"name": "Nhập môn Môi trường", "code": "ENV101", "credits": 3, "type": "offline"},
    {"name": "Biến đổi khí hậu", "code": "CC202", "credits": 2, "type": "online"},
    {"name": "Năng lượng tái tạo", "code": "RE303", "credits": 3, "type": "hybrid"},
    {"name": "Quản lý rác thải", "code": "WM404", "credits": 2, "type": "offline"},
    {"name": "Nông nghiệp bền vững", "code": "SA505", "credits": 3, "type": "offline"},
    {"name": "Kinh tế xanh", "code": "GE606", "credits": 2, "type": "online"},
    {"name": "Bảo tồn đa dạng sinh học", "code": "BD707", "credits": 3, "type": "hybrid"}
]

def generate_vietnamese_address(district):
    streets = [
        "Nguyễn Văn Linh", "Lê Duẩn", "Hùng Vương", "Bạch Đằng", "Trần Phú",
        "Nguyễn Tất Thành", "Điện Biên Phủ", "Ngô Quyền", "Võ Văn Kiệt", "Hoàng Diệu"
    ]
    num = random.randint(1, 999)
    street = random.choice(streets)
    return f"{num} {street}, Quận {district}, Đà Nẵng"

def generate_coordinates():
    # Da Nang coordinates roughly
    lat = 16.0 + random.uniform(0, 0.1)
    lng = 108.1 + random.uniform(0, 0.2)
    return lat, lng

async def seed_data():
    print("🌱 Bắt đầu tạo dữ liệu mẫu (Tiếng Việt)...")
    
    async with httpx.AsyncClient() as client:
        # Check health
        try:
            resp = await client.get(f"http://localhost:8008/health")
            if resp.status_code != 200:
                print("❌ Education Service chưa sẵn sàng!")
                return
        except Exception as e:
            print(f"❌ Không thể kết nối đến Education Service: {e}")
            return

        schools_created = 0
        
        for i in range(30):
            district = random.choice(DISTRICTS)
            school_type = random.choice(SCHOOL_TYPES)
            name = f"Trường {school_type} {random.choice(SCHOOL_NAMES)}"
            address = generate_vietnamese_address(district)
            lat, lng = generate_coordinates()
            
            school_facilities_list = random.sample(FACILITIES, k=random.randint(2, 6))
            
            school_data = {
                "name": name,
                "code": f"SCH-{random.randint(1000, 9999)}-{i}",
                "address": address,
                "latitude": lat,
                "longitude": lng,
                "type": school_type,
                "contact_email": f"contact{i}@school.edu.vn",
                "phone_number": f"0236{random.randint(100000, 999999)}",
                "website": f"https://school{i}.edu.vn",
                "facilities": {"items": school_facilities_list},
                "meta_data": {"district": district, "founded": random.randint(1950, 2020)}
            }
            
            try:
                # Create School
                resp = await client.post(f"{API_URL}/schools", json=school_data)
                if resp.status_code in [200, 201]:
                    school = resp.json()
                    school_id = school["id"]
                    print(f"✅ Đã tạo: {name}")
                    
                    # Add Courses
                    num_courses = random.randint(1, 5)
                    selected_courses = random.sample(COURSES, k=num_courses)
                    
                    for course in selected_courses:
                        course_data = course.copy()
                        course_data["school_id"] = school_id
                        # Randomize code slightly to avoid unique constraint if needed (though code is per school usually)
                        course_data["code"] = f"{course['code']}-{random.randint(10, 99)}"
                        
                        await client.post(f"{API_URL}/green-courses", json=course_data)
                    
                    # Calculate Score
                    await client.post(f"{API_URL}/schools/{school_id}/calculate-score")
                    
                    schools_created += 1
                else:
                    print(f"⚠️ Lỗi tạo trường {name}: Status {resp.status_code} - {resp.text}")
                    
            except Exception as e:
                print(f"❌ Lỗi: {e}")

        print(f"\n✨ Hoàn tất! Đã tạo {schools_created} trường học.")

if __name__ == "__main__":
    asyncio.run(seed_data())
