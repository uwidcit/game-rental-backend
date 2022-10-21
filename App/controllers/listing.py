from App.models import Game, Listing, Customer, Staff
from App.database import db

def get_available_listing(listingId):
    return Listing.query.filter_by(listingId=listingId, status='available').first()

def get_user_listings_by_status(userId, status):
    owner = Customer.query.get(userId)
    if owner :
        return Listing.query.filter_by(userId=userId, status=status)
    return f'{userId} user not found'

# filter vs filter_by https://stackoverflow.com/questions/8561470/sqlalchemy-filtering-by-relationship-attribute
def get_available_listings(platform):
    if platform :
      return Listing.query.filter(Game.platform==platform, Listing.status=="available").all()
    return Listing.query.filter_by(status='available').all()

def get_avaiable_listings_json(platform):
    listings = get_available_listings(platform)
    print(listings)
    if listings:
        return [ listing.toJSON_with_game() for listing in listings ]
    return []

# get all listings of the user for any status
def get_user_listings(userId):
    owner = Customer.query.get(userId)
    if owner :
        return owner.listings
    return f'{userId} user not found'

# creates a listing for a user
def list_game(staffId, userId, gameId, condition="good", price=10.00):
    owner = Customer.query.get(userId)
    game = Game.query.get(gameId)
    staff = Staff.query.get(staffId)
    if owner and game and staff:
        return staff.list_game(owner, game, condition, price)     
    return False

def delist_game(staffId, listingId):
    staff = Staff.query.get(staffId)
    listing = Listing.query.get(listingId)
    if listing and staff :
        return staff.delist_game(listing)
    return False

def get_listing(id):
    return Listing.query.get(id)

def get_all_listings():
    return Listing.query.all()