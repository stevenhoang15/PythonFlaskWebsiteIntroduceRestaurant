from model import AdminAccount, db
from werkzeug.security import generate_password_hash
from app import app  # Giả sử bạn có app Flask trong file app.py

# Bắt đầu ngữ cảnh ứng dụng Flask
with app.app_context():
# Tạo một AdminAccount mới
    new_admin = AdminAccount(
        name="Admin",
        password=generate_password_hash("123"),
        about="Some info about the admin",
        country="Country",
        address="Address",
        phone="123456789",
        email="admin@example.com",
        linkTwitter="https://twitter.com",
        linkFacebook="https://facebook.com",
        linkInstragram="https://instagram.com",
        linkLinkedin="https://linkedin.com",
        image="static/admin/img/admin.jpg"
    )

    # Thêm vào cơ sở dữ liệu
    db.session.add(new_admin)
    db.session.commit()

    print("Admin account created successfully!")
