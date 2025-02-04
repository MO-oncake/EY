# event_routes.py
from .common_imports import *
from models.event_ticket_type import EventTicketType
from models.event_date import EventDate
from models.event_ticket_count import EventTicketCount
from models.event import Event
from extensions import db

event_bp = Blueprint('event_bp', __name__)

# Routes for Events
@event_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_data = []
    for event in events:
        # Fetch the event date from the EventDate table
        event_date = EventDate.query.filter_by(event_id=event.id).first()
        date = event_date.event_date.strftime('%Y-%m-%d') if event_date else None
        
        # Fetch the ticket counts from the EventTicketCount table
        ticket_counts = EventTicketCount.query.filter_by(event_id=event.id).all()
        ticket_data = []
        for count in ticket_counts:
            ticket_data.append({
                "tier": count.tier,
                "total_count": count.total_count,
                "available_count": count.available_count,
                "total_purchased": count.total_purchased
            })

        # Fetch the ticket types (tiers) and prices from the EventTicketType table
        ticket_types = EventTicketType.query.filter_by(event_id=event.id).all()
        ticket_types_data = []
        for ticket in ticket_types:
            ticket_types_data.append({
                "tier_name": ticket.tier_name,
                "price": ticket.price
            })
        
        events_data.append({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "venue": event.venue,
            "time": event.time.strftime('%H:%M') if event.time else None,
            "image_url": event.image_url,
            "date": date,
            "ticket_counts": ticket_data,  # Added ticket counts for each tier
            "ticket_types": ticket_types_data  # Added ticket types and prices
        })
    return jsonify(events_data), 200

@event_bp.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get(id)
    if event:
        # Fetch the event date from the EventDate table
        event_date = EventDate.query.filter_by(event_id=event.id).first()
        date = event_date.event_date.strftime('%Y-%m-%d') if event_date else None
        
        # Fetch the ticket counts from the EventTicketCount table
        ticket_counts = EventTicketCount.query.filter_by(event_id=event.id).all()
        ticket_data = []
        for count in ticket_counts:
            ticket_data.append({
                "tier": count.tier,
                "total_count": count.total_count,
                "available_count": count.available_count,
                "total_purchased": count.total_purchased
            })

        # Fetch the ticket types (tiers) and prices from the EventTicketType table
        ticket_types = EventTicketType.query.filter_by(event_id=event.id).all()
        ticket_types_data = []
        for ticket in ticket_types:
            ticket_types_data.append({
                "tier_name": ticket.tier_name,
                "price": ticket.price
            })
        
        return jsonify({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "venue": event.venue,
            "time": event.time.strftime('%H:%M') if event.time else None,
            "image_url": event.image_url,
            "date": date,
            "ticket_counts": ticket_data,  # Added ticket counts for each tier
            "ticket_types": ticket_types_data  # Added ticket types and prices
        }), 200
    return jsonify({"message": "Event not found"}), 404

@event_bp.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()

    # Create the event
    new_event = Event(
        name=data.get('name'),
        description=data.get('description'),
        venue=data.get('venue'),
        time=data.get('time'),
        image_url=data.get('image_url'),
        organiser_id=data.get('organiser_id', 1)  # Default to organiser 1
    )
    db.session.add(new_event)
    db.session.commit()

    # Create the event date in the EventDate table
    event_date = data.get('event_date')
    if event_date:
        new_event_date = EventDate(event_id=new_event.id, event_date=event_date)
        db.session.add(new_event_date)
        db.session.commit()

    # Create ticket counts and types for the event
    ticket_counts_data = data.get('ticket_counts', [])
    for ticket_count in ticket_counts_data:
        ticket_count_entry = EventTicketCount(
            event_id=new_event.id,
            tier=ticket_count.get('tier'),
            total_count=ticket_count.get('total_count'),
            available_count=ticket_count.get('available_count'),
            total_purchased=0  # Initially 0 tickets purchased
        )
        db.session.add(ticket_count_entry)

    ticket_types_data = data.get('ticket_types', [])
    for ticket_type in ticket_types_data:
        ticket_type_entry = EventTicketType(
            event_id=new_event.id,
            tier_name=ticket_type.get('tier_name'),
            price=ticket_type.get('price')
        )
        db.session.add(ticket_type_entry)

    db.session.commit()

    return jsonify({"message": "Event created successfully!"}), 201

@event_bp.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.get_json()
    event = Event.query.get(id)
    if event:
        # Update event details
        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.venue = data.get('venue', event.venue)
        event.time = data.get('time', event.time)
        event.image_url = data.get('image_url', event.image_url)
        db.session.commit()

        # Update the event date in the EventDate table
        event_date = data.get('event_date')
        if event_date:
            existing_event_date = EventDate.query.filter_by(event_id=event.id).first()
            if existing_event_date:
                existing_event_date.event_date = event_date
            else:
                new_event_date = EventDate(event_id=event.id, event_date=event_date)
                db.session.add(new_event_date)
            db.session.commit()

        # Update ticket counts and types for the event
        ticket_counts_data = data.get('ticket_counts', [])
        for ticket_count in ticket_counts_data:
            existing_ticket_count = EventTicketCount.query.filter_by(
                event_id=event.id, tier=ticket_count.get('tier')).first()
            if existing_ticket_count:
                existing_ticket_count.total_count = ticket_count.get('total_count', existing_ticket_count.total_count)
                existing_ticket_count.available_count = ticket_count.get('available_count', existing_ticket_count.available_count)
                existing_ticket_count.total_purchased = ticket_count.get('total_purchased', existing_ticket_count.total_purchased)
            else:
                new_ticket_count_entry = EventTicketCount(
                    event_id=event.id,
                    tier=ticket_count.get('tier'),
                    total_count=ticket_count.get('total_count'),
                    available_count=ticket_count.get('available_count'),
                    total_purchased=0  # Initially 0 tickets purchased
                )
                db.session.add(new_ticket_count_entry)

        ticket_types_data = data.get('ticket_types', [])
        for ticket_type in ticket_types_data:
            existing_ticket_type = EventTicketType.query.filter_by(
                event_id=event.id, tier_name=ticket_type.get('tier_name')).first()
            if existing_ticket_type:
                existing_ticket_type.price = ticket_type.get('price', existing_ticket_type.price)
            else:
                new_ticket_type_entry = EventTicketType(
                    event_id=event.id,
                    tier_name=ticket_type.get('tier_name'),
                    price=ticket_type.get('price')
                )
                db.session.add(new_ticket_type_entry)

        db.session.commit()

        return jsonify({"message": "Event updated successfully!"}), 200
    return jsonify({"message": "Event not found"}), 404

@event_bp.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()

        # Also delete the associated event date
        event_date = EventDate.query.filter_by(event_id=event.id).first()
        if event_date:
            db.session.delete(event_date)
            db.session.commit()

        return jsonify({"message": "Event deleted successfully!"}), 200
    return jsonify({"message": "Event not found"}), 404

# Routes for EventDate
@event_bp.route('/event_dates', methods=['GET'])
def get_event_dates():
    dates = EventDate.query.all()
    dates_data = [{"event_id": date.event_id, "event_date": date.event_date} for date in dates]
    return jsonify(dates_data), 200

@event_bp.route('/event_dates/<int:event_id>', methods=['GET'])
def get_event_dates_by_event(event_id):
    dates = EventDate.query.filter_by(event_id=event_id).all()
    if dates:
        dates_data = [{"event_id": date.event_id, "event_date": date.event_date} for date in dates]
        return jsonify(dates_data), 200
    return jsonify({"message": "No dates found for this event"}), 404

@event_bp.route('/event_dates', methods=['POST'])
def create_event_date():
    data = request.get_json()
    new_date = EventDate(
        event_id=data.get('event_id'),
        event_date=data.get('event_date')
    )
    db.session.add(new_date)
    db.session.commit()
    return jsonify({"message": "Event date created successfully!"}), 201