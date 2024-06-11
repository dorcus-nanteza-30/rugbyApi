from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    user_type = db.Column(db.String(20), default='admin')
    join_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    membership_status = db.Column(db.String(50), nullable=False)

    # relationships
    team_members = db.relationship("TeamMember", back_populates="user")
    orders = db.relationship("Order", back_populates="user")
    donations = db.relationship("Donation", back_populates="user")

    def __init__(self, first_name, last_name, contact, email, password, user_type, membership_status, join_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.user_type = user_type
        self.membership_status = membership_status
        self.join_date = join_date or datetime.utcnow()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
