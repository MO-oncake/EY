from . import db

class EventTicketType(db.Model):
    __tablename__ = 'event_ticket_types'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    tier_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)