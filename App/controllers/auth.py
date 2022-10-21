from flask_jwt import JWT
from App.models import User, Staff, Customer


def authenticate(username, password):
    staff = Staff.query.filter_by(username=username).first()
    if staff and staff.check_password(password):
        return staff
    customer = Customer.query.filter_by(username=username).first()
    if customer and customer.check_password(password):
        return customer
    return None


# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    staff = Staff.query.get(payload['identity'])
    if staff:
        return staff
    customer = Customer.query.get(payload['identity'])
    if customer:
        return customer
    return None


def setup_jwt(app):
    return JWT(app, authenticate, identity)