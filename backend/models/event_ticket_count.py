from . import db

class EventTicketCount(db.Model):
    __tablename__ = 'event_ticket_count'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    tier = db.Column(db.String, primary_key=True)
    total_count = db.Column(db.Integer, nullable=False)
    available_count = db.Column(db.Integer, nullable=False)
    total_purchased = db.Column(db.Integer, default=0)