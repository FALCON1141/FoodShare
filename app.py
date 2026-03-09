from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Donation
import random
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET','POST'])
def register():

    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        code = str(random.randint(100000,999999))

        user = User(
            name=name,
            email=email,
            password=password,
            address=address,
            role="donor",
            verification_code=code
        )

        db.session.add(user)
        db.session.commit()

        return render_template("verify.html", code=code)

    return render_template("register.html")


@app.route('/verify', methods=['POST'])
def verify():

    code = request.form['code']

    user = User.query.filter_by(verification_code=code).first()

    if user:
        user.verified = True
        db.session.commit()
        return redirect(url_for('login'))

    return "Invalid verification code"


@app.route('/login', methods=['GET','POST'])
def login():

    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user and user.verified:

            session.permanent = True
            session['user_id'] = user.id

            return redirect(url_for('dashboard'))

        if user and not user.verified:
            return "Please verify your email first."

        return "Invalid email or password"

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    total = Donation.query.filter_by(donor_id=user_id).count()

    pending = Donation.query.filter_by(
        donor_id=user_id,
        status="Pending"
    ).count()

    completed = Donation.query.filter_by(
        donor_id=user_id,
        status="Completed"
    ).count()

    return render_template(
        "dashboard.html",
        total=total,
        pending=pending,
        completed=completed
    )


@app.route('/create_donation', methods=['GET','POST'])
def create_donation():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        food_type = request.form['food_type']
        quantity = request.form['quantity']
        pickup_location = request.form['pickup_location']
        expiry_time = request.form['expiry_time']

        donation = Donation(
            food_type=food_type,
            quantity=quantity,
            pickup_location=pickup_location,
            expiry_time=expiry_time,
            donor_id=session['user_id'],
            status="Pending"
        )

        db.session.add(donation)
        db.session.commit()

        return redirect(url_for('donation_history'))

    return render_template("create_donation.html")


@app.route('/donation_history')
def donation_history():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    donations = Donation.query.filter_by(
        donor_id=session['user_id']
    ).all()

    return render_template("donation_history.html", donations=donations)


@app.route('/edit_donation/<int:id>', methods=['GET','POST'])
def edit_donation(id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    donation = Donation.query.get(id)

    if donation.donor_id != session['user_id']:
        return "Unauthorized"

    if request.method == 'POST':

        donation.food_type = request.form['food_type']
        donation.quantity = request.form['quantity']
        donation.pickup_location = request.form['pickup_location']
        donation.expiry_time = request.form['expiry_time']

        db.session.commit()

        return redirect(url_for('donation_history'))

    return render_template("edit_donation.html", donation=donation)


@app.route('/delete_donation/<int:id>')
def delete_donation(id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    donation = Donation.query.get(id)

    if donation.donor_id != session['user_id']:
        return "Unauthorized"

    db.session.delete(donation)
    db.session.commit()

    return redirect(url_for('donation_history'))


@app.route('/profile')
def profile():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    return render_template("profile.html", user=user)


@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':

        user.name = request.form['name']
        user.email = request.form['email']
        user.address = request.form['address']

        db.session.commit()

        return redirect(url_for('profile'))

    return render_template("edit_profile.html", user=user)


@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)