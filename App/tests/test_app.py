import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db, db
from App.models import User, Staff
from App.controllers import (
    create_staff,
    get_staff,
    get_all_users_json,
    authenticate,
    get_user_by_username,
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
        # hashed = generate_password_hash(password, method='script')
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
    user = create_staff("bob", "bobpass")
    assert authenticate("bob", "bobpass")

def test_create_staff():
    ron = create_staff("ron", "bobpass")
    user = get_staff(ron.id)
    assert user.username == ron.username

class UsersIntegrationTests(unittest.TestCase):

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob", "type":"staff"}, {"id":2, "username":"ron", "type":"staff"}], users_json)

    def test_update_staff(self):
        update_staff(1, "ronnie")
        user = get_staff(1)
        assert user.username == "ronnie"

