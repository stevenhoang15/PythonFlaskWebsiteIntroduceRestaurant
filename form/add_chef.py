from model import Chef, db

def handle_chef_form(request):
    name = request.form['name']
    description = request.form['description']
    image = request.form['image']

    new_chef = Chef(name=name, description=description, image=image)
    
    try:
        db.session.add(new_chef)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error when adding chef: {e}")
        return False
