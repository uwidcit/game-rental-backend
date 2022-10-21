from App.models import User, Staff, Customer
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None
    

def create_staff(username, password):
    newuser = Staff(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None

def create_customer(username, password):
    newuser = Customer(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_staff(id):
    return Staff.query.get(id)

def get_customer(id):
    return Customer.query.get(id)

def is_staff(id):
    return Staff.query.get(id) != None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    staff = Staff.query.all()
    customers = Customer.query.all()
    users = []
    if not (staff or customers):
        return []
    
    for s in staff:
        users.append(s.toJSON())
    
    for c in customers:
        users.append(c.toJSON())
    
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    