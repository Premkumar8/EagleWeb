from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# Secret key for session management (e.g., flash messages)
app.config['SECRET_KEY'] = '77913021e79a2ed785e260eae8674997'

# Database configuration (using SQLite for simplicity)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'eagle.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration (replace with your email provider's details)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # e.g., 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'premkumarsuresh@gmail.com' # Your email address
app.config['MAIL_PASSWORD'] = 'olqmlwhrrannbnwv' # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'premkumarsuresh@gmail.com'

# --- INITIALIZATIONS ---
db = SQLAlchemy(app)
mail = Mail(app)

# --- DATABASE MODEL ---
class Contact(db.Model):
    """Represents a contact form submission in the database."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

# --- ROUTES ---
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Create a new contact record
        new_contact = Contact(name=name, email=email, message=message)
        
        try:
            # Add to database
            db.session.add(new_contact)
            db.session.commit()

            # Send email (optional)
            msg = Message(
                subject=f"New Contact Form Submission from {name}",
                recipients=['admin-email@example.com'],
                body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            )
            mail.send(msg)

            # Flash success message
            flash('Successfully submitted. We will contact you shortly.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred. Please try again. Error: {e}', 'danger')

        return redirect(url_for('index') + '#contact')

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
