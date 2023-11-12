import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db, db
from App.models import User, Staff
from App.controllers import (
    create_customer,
    create_game,
    get_customer,
    create_staff,
    get_all_users_json,
    authenticate,
    get_staff,
    get_game,
    get_rental,
    get_staff,
    create_game,
    get_all_users_json,
    authenticate,
    get_listing,
    update_staff
)

app = create_app({"SQLALCHEMY_DATABASE_URI":'sqlite:///test_database.db', "TESTING":True, "DEBUG":True})


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = Staff("bob", "bobpass")
        assert user.username == "bob"

    def test_toJSON(self):
        user = Staff("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "type": 'staff'})
    
    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    create_db(app)
    yield app.test_client()
    db.session.remove()
    db.drop_all()


def test_authenticate():
    bob = create_staff("bob", "bobpass")
    assert authenticate("bob", "bobpass")

def test_create_game():
    game = create_game("frogger", 1)
    assert game.title == "frogger" and game.rawgId == 1

def test_create_user():
    user = create_customer("rick", "bobpass")
    assert user.username == "rick"
    user = create_staff("bob", "bobpass")
    assert authenticate("bob", "bobpass")

def test_create_staff():
    ron = create_staff("ron", "bobpass")
    user = get_staff(ron.id)
    assert user.username == ron.username


def test_staff_create_listing():
    bob = get_staff(1)
    rick = get_customer(1)
    game = get_game(1)
    bob.list_game(rick, game, "new", 10)
    assert rick.listings[0].listingId == 1

def test_staff_confirm_rental():
    bob = get_staff(1)
    sally = create_customer("sally", "bobpass")
    listing = get_listing(1)
    bob.confirm_rental(sally, listing)
    assert listing.rentals[0].rentalId == 1

def test_staff_confirm_return():
    bob = get_staff(1)
    rental = get_rental(1)
    bob.confirm_return(rental)
    assert rental.return_date != None

# class UsersIntegrationTests(unittest.TestCase):

#     def test_get_all_users_json(self):
#         users_json = get_all_users_json()
#         self.assertListEqual([{"id":1, "username":"bob", "type":"staff"}, {"id":2, "username":"ron", "type":"staff"}], users_json)

    # tests staff's ability to create rentals in system
    # def test_list_game(self):
    #     bob = get_staff(1)
    #     jane = create_customer("jane", "janepass")
        
    #     game = create_game("frogger", 12324, "Teen", "NSW", "http://image.com", "adventure")
    #     new_listing = bob.list_game(jane, game, "good", 5.00)
    #     test_listing = get_listing(new_listing.listingId)
    #     assert test_listing.ownerId == jane.id and test_listing.gameId == game.gameId
    
    # def test_staff_confirm_rental(self):
    #     listing = get_listing(1)
    #     bob = get_staff(1)
    #     ross = create_customer("ross", "rosspass")
    #     new_rental = bob.confirm_rental(ross, listing)
    #     test_rental = get_rental(new_rental.rentalId)
    #     assert test_rental.renterId == ross.id and test_rental.listingId == listing.listingId
    
    # def test_staff_confirm_return(self):
    #     rental = get_rental(1)
    #     bob = get_staff(1)
    #     bob.confirm_return(rental)
    #     test_rental = get_rental(1)
    #     assert test_rental.return_date != None
        

    


        

        

