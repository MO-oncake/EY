from . import db

class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)