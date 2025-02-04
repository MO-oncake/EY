from . import db

class EventDate(db.Model):
    __tablename__ = 'event_dates'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)