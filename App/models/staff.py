from .user import User
from .listing import Listing
from .rental import Rental
from .rental_payment import RentalPayment
from App.database import db

class Staff(User):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.user_type = "staff"

    #passing objects instead of ids to avoid id not found error
    def list_game(self, owner, game, condition, price):
        try:
            listing = Listing(owner.id, game.gameId, condition, price)
            db.session.add(listing)
            db.session.commit()
            return listing
        except Exception as e:
            print('error creating listing', e)
            db.session.rollback()
            return None
    
    def delist_game(self, listing):
        try:
            listing.status = 'delisted'
            db.session.add(listing)
            db.session.commit()
            return True
        except:
            db.session.rollback()
        return False
    
    #assumes listing is valid and available
    def confirm_rental(self, renter, listing):
        rental = Rental(renter.id, listing.listingId)
        payment = RentalPayment(rental)
        listing.status = 'rented'
        try:
            db.session.add(rental)
            db.session.add(payment)
            db.session.add(listing)
            db.session.commit()
            return rental
        except Exception as e:
            print(e)
            return None
    
    def confirm_return(self, rental):
        # fees = rental.return_rental()
        # rental_payment = RentalPayment(rental)
        listing = Listing.query.get(rental.listingId)
        listing.status = 'available'
        try:
            db.session.add(listing)
            # db.session.add(rental_payment)
            db.session.commit()
            return 0
        except:
            return None
    
    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username,
            'type': 'staff'
        }