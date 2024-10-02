from routes import create_app  # Nhập hàm create_app từ routes
from model import db  # Nhập đối tượng db từ model

# Khởi tạo ứng dụng Flask
app = create_app()

# Tạo tất cả bảng trong cơ sở dữ liệu
with app.app_context():
    db.create_all()

