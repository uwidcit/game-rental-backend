from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), nullable=False, unique=True)
    user_type =  db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': user_type}


    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username
        }
