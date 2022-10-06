from App.models import User, Game, Listing
from App.database import db


def get_user_listings_by_status(userId, status):
    user = User.query.get(userId)
    if userId :
        return Listing.query.filter_by(userId =userId, status=status)
    return f'{userId} user not found'

def get_available_listings():
    return Listing.query.filter_by(status='available').all()

def get_avaiable_listings_json():
    listings = get_available_listings()
    json = [ listing.toJSON_with_game() for listing in listings ]

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
        # check if user already has a listing for this game
        listing = Listing.query.filter_by(userId=userId, gameId=gameId).first()     
        
        #if user does not already have this game listed
        if listing == None:
            listing = Listing(userId, gameId, condition, price)
            db.session.add(listing)
            db.session.commit() 
            return True
    # operation failed, ids might be invalid or listing already exists         
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