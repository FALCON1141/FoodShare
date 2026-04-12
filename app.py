from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Donation, Review, ContactMessage
from datetime import timedelta, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db.init_app(app)

with app.app_context():
    db.create_all()

def parse_date_safe(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None


@app.route('/')
def home():
    return render_template("home.html",
        total=Donation.query.count(),
        distributed=Donation.query.filter_by(status="Distributed").count(),
        volunteers=User.query.filter_by(role="volunteer").count(),
        reviews=Review.query.all()
    )


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db.session.add(User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            address=request.form['address'],
            role=request.form['role']
        ))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
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


@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'donor':
        return redirect(url_for('login'))

    return render_template("dashboard.html",
        total=Donation.query.filter_by(donor_id=session['user_id']).count(),
        pending=Donation.query.filter_by(donor_id=session['user_id'], status="Pending").count(),
        completed=Donation.query.filter_by(donor_id=session['user_id'], status="Distributed").count()
    )

@app.route('/create_donation', methods=['GET','POST'])
def create_donation():
    if session.get('role') != 'donor':
        return redirect(url_for('login'))

    if request.method == 'POST':
        db.session.add(Donation(
            food_type=request.form['food_type'],
            quantity=int(request.form['quantity']),
            pickup_location=request.form['pickup_location'],
            expiry_time=parse_date_safe(request.form['expiry_time']),
            donor_id=session['user_id']
        ))
        db.session.commit()
        return redirect(url_for('donation_history'))

    return render_template("create_donation.html")

@app.route('/donation_history')
def donation_history():
    if session.get('role') != 'donor':
        return redirect(url_for('login'))

    return render_template("donation_history.html",
        donations=Donation.query.filter_by(donor_id=session['user_id']).all()
    )

@app.route('/edit_donation/<int:id>', methods=['GET','POST'])
def edit_donation(id):
    d = Donation.query.get(id)

    if d.status in ["Accepted", "Assigned"]:
        return "Locked"

    if request.method == 'POST':
        d.food_type = request.form['food_type']
        d.quantity = int(request.form['quantity'])
        d.pickup_location = request.form['pickup_location']
        d.expiry_time = parse_date_safe(request.form['expiry_time'])
        db.session.commit()
        return redirect(url_for('donation_history'))

    return render_template("edit_donation.html", donation=d)

@app.route('/delete_donation/<int:id>')
def delete_donation(id):
    d = Donation.query.get(id)

    if d.status in ["Accepted", "Assigned"]:
        return "Locked"

    db.session.delete(d)
    db.session.commit()
    return redirect(url_for('donation_history'))

@app.route('/my_messages')
def my_messages():

    if not session.get('user_id'):
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    messages = ContactMessage.query.filter_by(email=user.email).all()

    return render_template("my_messages.html", messages=messages)

@app.route('/volunteer')
def volunteer_dashboard():
    if session.get('role') != 'volunteer':
        return redirect(url_for('login'))

    assigned = Donation.query.filter_by(volunteer_id=session['user_id']).all()

    return render_template("volunteer_dashboard.html",
        available=Donation.query.filter_by(volunteer_id=None).all(),
        assigned=assigned,
        total=len(assigned),
        pending=len([d for d in assigned if d.status in ["Assigned", "Accepted", "Collected"]]),
        completed=len([d for d in assigned if d.status == "Distributed"])
    )

@app.route('/accept/<int:id>')
def accept(id):
    d = Donation.query.get(id)


    if d.volunteer_id != session.get('user_id'):
        return "Unauthorized"

    d.status = "Accepted"
    db.session.commit()

    return redirect(url_for('volunteer_dashboard'))

@app.route('/reject/<int:id>')
def reject(id):
    d = Donation.query.get(id)

    if d.volunteer_id != session.get('user_id'):
        return "Unauthorized"

    d.volunteer_id = None
    d.status = "Pending"

    db.session.commit()
    return redirect(url_for('volunteer_dashboard'))

@app.route('/collect/<int:id>')
def collect(id):
    d = Donation.query.get(id)
    d.status = "Collected"
    db.session.commit()
    return redirect('/volunteer')

@app.route('/complete/<int:id>')
def complete(id):
    d = Donation.query.get(id)
    d.status = "Distributed"
    db.session.commit()
    return redirect('/volunteer')

@app.route('/volunteer_history')
def volunteer_history():
    if session.get('role') != 'volunteer':
        return redirect(url_for('login'))

    history = Donation.query.filter_by(
        volunteer_id=session['user_id']
    ).all()

    return render_template("volunteer_history.html", history=history)


@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    return render_template("admin_dashboard.html",
        donations=Donation.query.all(),
        users=User.query.all(),
        volunteers=User.query.filter_by(role="volunteer").all()
    )

@app.route('/toggle_user/<int:id>')
def toggle_user(id):
    u = User.query.get(id)
    u.active = not u.active
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/assign/<int:donation_id>/<int:volunteer_id>')
def assign(donation_id, volunteer_id):

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    d = Donation.query.get(donation_id)

    if d.status in ["Accepted", "Collected", "Distributed"]:
        return "Cannot reassign. Task already in progress or completed."

    d.volunteer_id = volunteer_id
    d.status = "Assigned"

    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/messages')
def admin_messages():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    messages = ContactMessage.query.all()
    return render_template("admin_messages.html", messages=messages)

@app.route('/reply/<int:id>', methods=['POST'])
def reply_message(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    msg = ContactMessage.query.get(id)

    if msg:
        msg.reply = request.form['reply']
        db.session.commit()

    return redirect(url_for('admin_messages'))

@app.route('/admin/reply/<int:id>', methods=['GET','POST'])
def admin_reply(id):

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    msg = ContactMessage.query.get(id)

    if request.method == 'POST':
        msg.reply = request.form['reply']
        db.session.commit()
        return redirect(url_for('admin_messages'))

    return render_template("admin_reply.html", msg=msg)

@app.route('/admin/all_donations')
def all_donations():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    return render_template("all_donations.html",
        donations=Donation.query.all()
    )


@app.route('/contact', methods=['GET','POST'])
def contact():
    message_sent = False

    if request.method == 'POST':
        db.session.add(ContactMessage(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        ))
        db.session.commit()
        message_sent = True

    return render_template("contact.html", message_sent=message_sent)

@app.route('/add_review', methods=['POST'])
def add_review():
    db.session.add(Review(
        user_name=request.form['name'],
        message=request.form['message']
    ))
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if not user:
        return redirect(url_for('login'))

    if user.role == "donor":
        messages = ContactMessage.query.filter_by(email=user.email).all()
        
    return render_template("profile.html", user=user)

@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.address = request.form['address']

        db.session.commit()
        return redirect(url_for('profile'))

    return render_template("edit_profile.html", user=user)

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/faq')
def faq():
    return render_template("faq.html")

if __name__ == '__main__':
    app.run(debug=True)
