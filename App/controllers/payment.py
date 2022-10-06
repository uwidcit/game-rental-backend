from App.models import RentalPayment
from App.database import db

def create_rental_payment(amount, rentalId, userId):
    rental_payment = RentalPayment(rentalId, userId, amount)
    db.session.add(rental_payment)
    db.session.commit()
    return rental_payment