import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User
from App.controllers import (
    create_customer,
    create_game,
    get_user,
    get_customer,
    create_staff,
    get_all_users_json,
    authenticate,
    get_staff,
    update_user,
    get_game
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
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
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate():
    bob = create_staff("bob", "bobpass")
    assert authenticate("bob", "bobpass")

def test_create_game():
    game = create_game("frogger", 1)
    assert game.title == "frogger" and game.rawgId == 1

def test_create_user():
    user = create_customer("rick", "bobpass")
    assert user.username == "rick"

def test_create_game():
    user = create_staff("staff", "staffpass")
    user.create_game(1, "new game")
    assert user.games[0].rawgId == 1

def test_staff_create_listing():
    bob = get_staff(1)
    rick = get_customer(1)
    game = get_game(1)
    bob.create_listing(rick, game, "new", 10)
    assert rick.listings[0].listingId == 1

def test_staff_confirm_rental():
    user = create_staff("staff", "staffpass")
    user.confirm_rental(1)
    assert user.rentals[0].confirmed

def test_staff_confirm_return():
    user = create_staff("staff", "staffpass")
    user.confirm_return(1)
    assert user.rentals[0].returned

class UsersIntegrationTests(unittest.TestCase):

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
    
    def test_create_staff(self):
        user = create_staff("staff", "staffpass")
        print(user.id)
        assert user.username == "staff"
