from app import db # Assuming db is the SQLAlchemy object from app/__init__.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venue = db.Column(db.String(128))
    total_tickets = db.Column(db.Integer, nullable=False, default=0)
    available_tickets = db.Column(db.Integer, nullable=False, default=0)
    tickets = db.relationship('Ticket', backref='event', lazy='dynamic')

    def __repr__(self):
        return f'<Event {self.name}>'

# Association table for Order and Ticket (Many-to-Many)
order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    # user_id can be nullable if tickets are sold to guests or assigned later
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ticket_type = db.Column(db.String(64), default='General Admission')
    price = db.Column(db.Float, nullable=False, default=0.0)
    seat_information = db.Column(db.String(128), nullable=True) # e.g., "Section A, Row 10, Seat 5"
    is_sold = db.Column(db.Boolean, default=False, nullable=False)
    # No direct relationship to Order here, using the association table order_items

    def __repr__(self):
        return f'<Ticket {self.id} for Event {self.event_id}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    # Relationship to tickets via the association table
    tickets = db.relationship('Ticket', secondary=order_items,
                              backref=db.backref('orders', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'
