from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime



bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models statshot"""

class User(db.Model):
    """Site user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    username = db.Column(db.String, 
                         nullable=False,
                         unique=True)
    
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register (cls, username, password):
        """Register a user, hashing their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.  
        Return user if valid; else return false"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user 
        else: 
            return False

class Preference(db.Model):
    """User preferences"""

    __tablename__ = 'prefs'

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'),
                        primary_key=True, 
                        nullable=False
    )

    fav_team_id = db.Column(db.Integer)

class Login(db.Model):
    """Login timestamps"""

    __tablename__ = 'logins'
    login_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    time_stamp = db.Column(db.String,
                           nullable=False)

    @classmethod
    def record_login(cls, user_id):
        """Record login in database"""
    
        login = cls(
            user_id = user_id,
            time_stamp = datetime.datetime.now()
        )
        db.session.add(login)
        return login


    

    