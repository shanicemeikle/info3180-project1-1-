from . import db
class UserProfile(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(240))
    gender = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    profile_image=db.Column(db.String(80))
    created_on = db.Column(db.DateTime())
    #password = db.Column(db.String(255))

    def __init__(self, userid, firstname, lastname, age, gender, bio, username,profile_image, created_on):
        self.userid=userid
        self.firstname=firstname
        self.lastname=lastname
        self.age=age
        self.gender=gender
        self.bio=bio
        self.username=username
        self.profile_image=profile_image
        self.created_on=created_on
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
