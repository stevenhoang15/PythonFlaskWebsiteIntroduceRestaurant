# app/main/routes.py
from datetime import datetime
from flask import render_template, request, flash, Flask, redirect, url_for, session, Request
from model import MenuItem, db, Contact, AdminAccount, Chef, Booked, Event
#from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from form.add_chef import handle_chef_form
import os
import requests
import hashlib

def create_app():
    app = Flask(__name__)
    app.secret_key = "hello"
    # Cấu hình cơ sở dữ liệu
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/customer/img/menu'  # Nơi lưu trữ file upload
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn kích thước file upload (16MB)
    db.init_app(app)
    #login_manager = LoginManager(app=app)
    #login_manager.init_app(app)
    # login_manager.login_view = 'login'  # Chuyển hướng người dùng chưa login đến trang login
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return AdminAccount.query.get(int(user_id))
    
    @app.route('/')
    def index():
        events = Event.query.all()
        menu_items = MenuItem.query.all()
        return render_template('Customer/index.html', static_folder='static/customer', menu_items = menu_items, events = events)

    #admin_bp = Blueprint('admin', __name__, static_folder='static/admin', template_folder='templates/Admin')
    @app.route('/to-admin')
    def to_admin():
        # Redirect đến trang admin
        return redirect(url_for('admin_index'))

    # @app.route('/admin/login', methods=['GET', 'POST'])
    # def login():
    #     print("Da vao trang login")
    #     if request.method == 'POST':
    #         username = request.form.get('username')
    #         password = request.form.get('password')
    #         password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    #         # Kiểm tra thông tin đăng nhập
    #         admin = AdminAccount.query.filter(AdminAccount.name == username.strip(), AdminAccount.password == password.strip()).first()
    #         if admin:
    #             print("Password dung")
    #             login_user(admin)  # Thay vì dùng session
    #             return redirect(url_for('admin_index'))
    #         else:
    #             flash('Invalid username or password', 'danger')

    #     return redirect(url_for('admin_index'))
    
    @app.route('/admin')
    def admin_index():
        # print("Vao trang admin")
        # if not session.get('admin_logged_in'):
        #     print("Chuyen toi trang login")
        #     return redirect(url_for('login'))  # Nếu chưa đăng nhập thì chuyển tới trang login
        return render_template('Admin/index.html')

    # @app.before_request
    # def require_login():
    #     if request.endpoint.startswith('admin_') and not session.get('admin_logged_in'):
    #         return redirect(url_for('login'))

    # @app.route('/admin/logout')
    # def logout():
    #     session.pop('admin_logged_in', None)
    #     return redirect(url_for('login'))

    @app.route('/admin/menu')
    def admin_menu():
        menu_items = MenuItem.query.all()
        return render_template('Admin/menu.html', static_folder='static/customer', menu_items = menu_items)
    
    @app.route('/admin/menu/edit/<int:menu_id>', methods=['GET', 'POST'])
    def edit_menu(menu_id):
        menu_item = MenuItem.query.get_or_404(menu_id)

        if request.method == 'POST':
            # Cập nhật dữ liệu
            print(type(menu_item))
            menu_item.name = request.form.get('name', menu_item.name)
            menu_item.category = request.form.get('category', menu_item.category)
            #menu_item.description = request.form.get('description', menu_item.description)
            menu_item.price = request.form.get('price', menu_item.price)
            
            # Kiểm tra nếu người dùng cập nhật ảnh mới
            if 'image' in request.files:
                print("Image field found")
                file = request.files['image']
                if file and file.filename != '':  # Nếu có file và file không trống
                    print("File uploaded: ", file.filename)
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    menu_item.image = filename  # Cập nhật tên file ảnh mới
            
            db.session.commit()
            return redirect(url_for('admin_menu'))

        return render_template('Admin/edit_menu.html', menu_item=menu_item)


    @app.route('/admin/menu/delete/<int:menu_id>', methods=['POST'])
    def delete_menu(menu_id):
        menu_item = MenuItem.query.get_or_404(menu_id)
        db.session.delete(menu_item)
        db.session.commit()
        return redirect(url_for('admin_menu'))

    
    @app.route('/admin/menu/addmenu', methods=["post", "get"])
    def add_menu():    
        print("Request URL:", url_for('add_menu'))  # In URL kiểm tra
        print("Request method:", request.method)
        try:
            print("Request method:", request.method)
            #return render_template('Admin/add_menu.html')
            if request.method == "POST":
                print("hello")
                print("Request method:", request.method)
                # Kiểm tra xem người dùng có tải lên file không
                if 'image' not in request.files:
                    print("No image file part!", 'danger')
                    return redirect(request.url)

                file = request.files['image']
                
                if file.filename == '':
                    print("No selected file!", 'danger')
                    return redirect(request.url)

                if file:
                    # Lưu file vào thư mục đã cấu hình
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Lấy dữ liệu từ form
                name = request.form['name']
                category = request.form['category']
                description = request.form['description']
                price = float(request.form['price'])  # Đảm bảo rằng price là số thực
                image = request.files['image'].filename  # Tên file ảnh

                # Tạo một đối tượng MenuItem mới
                new_menu_item = MenuItem(
                    name=name, 
                    category=category, 
                    description=description, 
                    price=price, 
                    image=image
                )
                
                # Lưu menu item vào database
                db.session.add(new_menu_item)
                db.session.commit()

                print('Menu item added successfully!', 'success')
                return redirect(url_for('add_menu'))  # Redirect hoặc render lại trang sau khi upload
            print("Request method:", request.method)
            print("Kh them duoc")
            return render_template('Admin/add_menu.html')
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('Admin/add_menu.html')
    
    @app.route('/admin/chef')
    def admin_chef():       
        chefs = Chef.query.all()
        return render_template('Admin/chef.html', static_folder='static/customer', chefs = chefs)
    
    @app.route('/admin/chef/delete/<int:chef_id>', methods=['POST'])
    def delete_chef(chef_id):
        c = Chef.query.get_or_404(chef_id)
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for('admin_chef'))

    @app.route('/admin/chef/edit/<int:chef_id>', methods=['GET', 'POST'])
    def edit_chef(chef_id):
        c = Chef.query.get_or_404(chef_id)
        #request.method = "post"
        if request.method == 'POST':
            # Cập nhật dữ liệu
            c.name = request.form['name']
            c.category = request.form['category']
            c.description = request.form['description']
            c.price = request.form['price']
            c.image = request.form['image']
            db.session.commit()
            return redirect(url_for('admin_menu'))
        
        return render_template('Admin/edit_menu.html', c = c)

    @app.route('/admin/chef/addchef', methods = ['get', 'post'])
    def add_chef():
        print("Request method:", request.method)
        try:
            print("Request method:", request.method)
            if request.method == 'post':
                if 'image' not in request.files:
                    print("No image file part!", 'danger')
                    return redirect(request.url)

                file = request.files['image']
                    
                if file.filename == '':
                    print("No selected file!", 'danger')
                    return redirect(request.url)

                if file:
                        # Lưu file vào thư mục đã cấu hình
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = request.form['name']
                description = request.form['description']
                image = request.form['image']

                new_chef = Chef(name=name, description=description, image=image)
        
                db.session.add(new_chef)
                db.session.commit()
                return redirect(url_for('add_chef'))
                # except Exception as e:
                #     db.session.rollback()
                #     print(f"Error when adding chef: {e}")
            print("Request method:", request.method)
            print("Kh them duoc")
            return render_template('Admin/add_chef.html')
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('Admin/add_chef.html')
        #     if handle_chef_form(request):
        #         flash('Your message has been sent successfully!', 'success')
        #     else:
        #         flash('Error: Unable to send your message.', 'danger')
        #     return redirect(url_for('add_chef'))
        # return render_template('Admin/add_chef.html')
        
        # print("method: " + request.method)  # Kiểm tra method là gì
        # print(request.form.get('name'))
        # if request.method == "POST":
        #     name = request.form['name']
        #     description = request.form['description']
        #     new_chef = Chef(name = name, description = description, image = "#")
        #     db.session.add(new_chef)
        #     db.session.commit()
        #     print("Add chef successfully")
        #     print("method: " + request.method)
        #     return redirect(url_for('admin_chef'))
        # return redirect(url_for('admin_chef'))

    @app.route('/admin/event')
    def admin_event():       
        events = Event.query.all()
        return render_template('Admin/event.html', events = events)
    
    @app.route('/admin/event/addevent', methods = ["GET", "POST"])
    def add_event():
        try:
            print("Request method:", request.method)
            #return render_template('Admin/add_menu.html')
            if request.method == "POST":
                print("hello")
                print("Request method:", request.method)
                # Kiểm tra xem người dùng có tải lên file không
                if 'image' not in request.files:
                    print("No image file part!", 'danger')
                    return redirect(request.url)

                file = request.files['image']
                
                if file.filename == '':
                    print("No selected file!", 'danger')
                    return redirect(request.url)

                if file:
                    # Lưu file vào thư mục đã cấu hình
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Lấy dữ liệu từ form
                name = request.form['name']
                description = request.form['description']
                image = request.files['image'].filename  # Tên file ảnh
                price = float(request.form['price'])  # Đảm bảo rằng price là số thực

                # Tạo một đối tượng MenuItem mới
                new_envent = Event(
                    name=name, 
                    description=description, 
                    image=image,
                    price=price
                )

                # Lưu menu item vào database
                db.session.add(new_envent)
                db.session.commit()

                print('Event added successfully!', 'success')
                return redirect(url_for('add_event'))  # Redirect hoặc render lại trang sau khi upload
            print("Request method:", request.method)
            print("Kh them duoc")
            return render_template('Admin/index.html')
        except Exception as e:
            db.session.rollback()
            print(e)

    @app.route('/admin/event/delete/<int:event_id>', methods=['POST'])
    def delete_event(event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('admin_event'))
    
    @app.route('/admin/event/edit/<int:event_id>', methods=['GET', 'POST'])
    def edit_event(event_id):
        event = Event.query.get_or_404(event_id)
        #request.method = "post"
        if request.method == 'POST':
            # Cập nhật dữ liệu
            event.name = request.form['name']
            event.description = request.form['description']
            event.image = request.form['image']
            event.price = request.form['price']
            db.session.commit()
            return redirect(url_for('admin_event'))
        
        return render_template('Admin/edit_event.html', event=event)

    @app.route('/admin/gallarey')
    def admin_gallarey():       
        return render_template('Admin/gallarey.html')
    
    @app.route('/admin/contact', methods=["GET", "POST"])
    def admin_contact():   
        # Lấy tất cả dữ liệu từ bảng Contact
        contacts = Contact.query.all()
        
        #GraphQL
        # query = """
        # {
        # contacts {
        #     id
        #     name
        #     email
        #     subject
        #     message
        # }
        # }
        # """
        
        # # Gửi yêu cầu tới GraphQL API
        # response = requests.post(
        #     'http://localhost:5000/graphql',  # Thay đổi URL nếu cần
        #     json={'query': query}
        # )

        # # Kiểm tra response từ API
        # data = response.json()
        # if "errors" in data:
        #     return "Error fetching contacts", 500

        # # Lấy danh sách contact
        # contacts = data['data']['contacts']
        # Render template và truyền dữ liệu contacts vào
        return render_template('admin/contact.html', contacts=contacts)    
    
    @app.route('/admin/contact/delete/<int:contact_id>', methods=['POST'])
    def delete_contact(contact_id):
        contact = Contact.query.get(contact_id)
        
        if contact:
            try:
                db.session.delete(contact)
                db.session.commit()
                flash('Contact deleted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error: Unable to delete contact.', 'danger')
        # #GrahpQL
        # mutation = """
        #     mutation {
        #     deleteContact(id: %d) {
        #         ok
        #     }
        #     }
        # """ % id
        
        # # Gửi yêu cầu tới GraphQL API
        # response = requests.post(
        #     'http://localhost:5000/graphql',
        #     json={'query': mutation}
        # )
        
        # # Kiểm tra kết quả
        # data = response.json()
        # if "errors" in data or not data['data']['deleteContact']['ok']:
        #     return "Error deleting contact", 500
        return redirect(url_for('admin_contact'))

    @app.route('/admin/booked', methods=["GET", "POST"])
    def admin_booked():     
        bookeds = Booked.query.all()  
        return render_template('Admin/booked.html', bookeds = bookeds)
    
    @app.route('/admin/booked/delete/<int:booked_id>', methods=['POST'])
    def delete_booked(booked_id):
        booked = Booked.query.get(booked_id)
        
        if booked:
            try:
                db.session.delete(booked)
                db.session.commit()
                flash('Booked deleted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error: Unable to delete booked.', 'danger')
        return redirect(url_for('admin_booked'))
    
    @app.route('/admin/user_profile')
    def admin_profile():       
        return render_template('Admin/admin_profile.html')
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():       
        if request.method == 'POST':
            print("Request method:", request.method)
            # Lấy dữ liệu từ form
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')

            # Tạo một record mới trong bảng Contact
            new_contact = Contact(name=name, email=email, subject=subject, message=message)
            try:
                db.session.add(new_contact)
                db.session.commit()
                print('Your message has been sent successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash('Error: Unable to send your message.', 'danger')
                print(e)
                return redirect(url_for('admin_index'))
        return render_template('Customer/index.html')
    
    @app.route('/booked', methods=['GET', 'POST'])
    def booked():       
        if request.method == 'POST':
            print("Request method:", request.method)
            # Lấy dữ liệu từ form
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            date = request.form.get('date')
            time = request.form.get('time')
            people = request.form.get('people')
            message = request.form.get('message')

            # Tạo một record mới trong bảng Contact
            new_booked = Booked(name=name, email=email, phone=phone, dayBooked = datetime.strptime(date, '%Y-%m-%d').date(), timeBooked = datetime.strptime(time, '%H:%M').time(), ofPeople = people, message=message)
            try:
                db.session.add(new_booked)
                db.session.commit()
                print('Your booked has been sent successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash('Error: Unable to send your booked.', 'danger')
                print(e)
                return redirect(url_for('admin_index'))
        return render_template('Customer/index.html')
    
    return app
    




