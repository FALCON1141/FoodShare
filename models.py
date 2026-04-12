from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

    address = db.Column(db.String(200))
    role = db.Column(db.String(50))

    active = db.Column(db.Boolean, default=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    message = db.Column(db.Text)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
    reply = db.Column(db.Text)


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    food_type = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    pickup_location = db.Column(db.String(200))
    expiry_time = db.Column(db.Date)

    status = db.Column(db.String(50), default="Pending")

    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    donor = db.relationship('User', foreign_keys=[donor_id])
    volunteer = db.relationship('User', foreign_keys=[volunteer_id])

    rejected_by = db.Column(db.String(200), default="")