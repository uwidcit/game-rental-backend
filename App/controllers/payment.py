from App.models import RentalPayment
from App.database import db

def create_rental_payment(rental):
    rental_payment = RentalPayment(rental)
    db.session.add(rental_payment)
    db.session.commit()
    return rental_payment