from . import db 

#includes one-to-many relationships - one user can have many posts, one post can have many comments
class Salesfigures(db.Model):
    # the variable id is a column of a unique int, used to look up users
    id = db.Column(db.Integer, primary_key = True)
    drinks_sold = db.Column(db.Integer())
    money_made = db.Column(db.Integer())
    mean = db.Column(db.Integer())
    