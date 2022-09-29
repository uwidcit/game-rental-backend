from App.models import User, Game, Listing
from App.database import db


def get_user_listings_by_status(userId, status):
    user = User.query.get(userId)
    if userId :
        return Listing.query.filter_by(userId =userId, status=status)
    return f'{userId} user not found'

def get_available_listings():
    return Listing.query.filter_by(status='available')

# get all listings of the user for any status
def get_user_listings(userId):
    user = User.query.get(userId)
    if userId :
        return user.listings
    return f'{userId} user not found'

# creates a listing for a user
def list_game(userId, gameId, condition="good", price=10.00):

    user = User.query.get(userId)
    game = Game.query.get(gameId)

    if user and game:
        listing = Listing.query.filter_by(userId=userId, gameId=gameId).first()     
        
        if listing == None:
            listing.status = 'available'
        else:
            listing = Listing(userId, gameId, condition, price)
        db.session.add(listing)
        db.session.commit()
        return True
    return False

def delist_game(listingId, userId):
    listing = Listing.query.filter_by(listingId=listingId, userId=userId).first()
    if listing :
        listing.status = 'delisted'
        db.session.add(listing)
        db.session.commit()
        return True
    return False

def get_all_listings():
    return Listing.query.all()