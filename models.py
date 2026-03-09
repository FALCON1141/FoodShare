from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

    address = db.Column(db.String(200))

    role = db.Column(db.String(50))

    verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    food_type = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    pickup_location = db.Column(db.String(200))
    expiry_time = db.Column(db.String(100))

    status = db.Column(db.String(50), default="Pending")

    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))