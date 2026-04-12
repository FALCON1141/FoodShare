print("🔥 app.py is running")

from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta, datetime

from models import db, User, Donation, Review, ContactMessage

app = Flask(__name__)

import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'database.db')
app.config['SECRET_KEY'] = 'secret123'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# SAFE DATE
def parse_date_safe(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None


# HOME
@app.route('/')
def home():
    return render_template(
        "home.html",
        total=Donation.query.count(),
        distributed=Donation.query.filter_by(status="Distributed").count(),
        volunteers=User.query.filter_by(role="volunteer").count(),
        reviews=Review.query.all()
    )


# AUTH
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            address=request.form['address'],
            role=request.form['role']
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        user = User.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()

        if user:

            if not user.active:
                return render_template("login.html", message="Blocked")

            session['user_id'] = user.id
            session['role'] = user.role

            if user.role == "admin":
                return redirect(url_for('admin_dashboard'))

            elif user.role == "volunteer":
                return redirect(url_for('volunteer_dashboard'))

            else:
                return redirect(url_for('dashboard'))

        return render_template("login.html", message="Invalid")

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# DONOR DASHBOARD
@app.route('/dashboard')
def dashboard():

    if session.get('role') != 'donor':
        return redirect(url_for('login'))

    return render_template(
        "dashboard.html",
        total=Donation.query.filter_by(donor_id=session['user_id']).count(),
        pending=Donation.query.filter_by(
            donor_id=session['user_id'],
            status="Pending"
        ).count(),
        completed=Donation.query.filter_by(
            donor_id=session['user_id'],
            status="Distributed"
        ).count()
    )


# CREATE DONATION
@app.route('/create_donation', methods=['GET', 'POST'])
def create_donation():

    if session.get('role') != 'donor':
        return redirect(url_for('login'))

    if request.method == 'POST':

        donation = Donation(
            food_type=request.form['food_type'],
            quantity=int(request.form['quantity']),
            pickup_location=request.form['pickup_location'],
            expiry_time=parse_date_safe(request.form['expiry_time']),
            donor_id=session['user_id']
        )

        db.session.add(donation)
        db.session.commit()

        return redirect(url_for('donation_history'))

    return render_template("create_donation.html")


# DONATION HISTORY
@app.route('/donation_history')
def donation_history():

    if session.get('role') != 'donor':
        return redirect(url_for('login'))

    donations = Donation.query.filter_by(
        donor_id=session['user_id']
    ).all()

    return render_template("donation_history.html", donations=donations)


# VOLUNTEER DASHBOARD
@app.route('/volunteer')
def volunteer_dashboard():

    if session.get('role') != 'volunteer':
        return redirect(url_for('login'))

    assigned = Donation.query.filter_by(
        volunteer_id=session['user_id']
    ).all()

    return render_template(
        "volunteer_dashboard.html",
        available=Donation.query.filter_by(volunteer_id=None).all(),
        assigned=assigned
    )


# ACCEPT DONATION
@app.route('/accept/<int:id>')
def accept(id):

    d = Donation.query.get(id)

    if d.volunteer_id != session.get('user_id'):
        return "Unauthorized"

    d.status = "Accepted"
    db.session.commit()

    return redirect(url_for('volunteer_dashboard'))


# ADMIN DASHBOARD
@app.route('/admin')
def admin_dashboard():

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    return render_template(
        "admin_dashboard.html",
        donations=Donation.query.all(),
        users=User.query.all(),
        volunteers=User.query.filter_by(role="volunteer").all()
    )


# ASSIGN VOLUNTEER
@app.route('/assign/<int:donation_id>/<int:volunteer_id>')
def assign(donation_id, volunteer_id):

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    d = Donation.query.get(donation_id)

    if d.status in ["Accepted", "Collected", "Distributed"]:
        return "Cannot reassign."

    d.volunteer_id = volunteer_id
    d.status = "Assigned"

    db.session.commit()

    return redirect(url_for('admin_dashboard'))


# CONTACT
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    message_sent = False

    if request.method == 'POST':

        msg = ContactMessage(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )

        db.session.add(msg)
        db.session.commit()

        message_sent = True

    return render_template("contact.html", message_sent=message_sent)


# ADD REVIEW
@app.route('/add_review', methods=['POST'])
def add_review():

    review = Review(
        user_name=request.form['name'],
        message=request.form['message']
    )

    db.session.add(review)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")

    app.run(debug=True)