# ticket_routes.py
from .common_imports import *
from models.event_ticket_type import EventTicketType
from models.event_ticket_count import EventTicketCount
from extensions import db

# Routes for EventTicketCount
@ticket_bp.route('/event_ticket_counts', methods=['GET'])
def get_event_ticket_counts():
    counts = EventTicketCount.query.all()
    counts_data = [{"event_id": count.event_id, "tier": count.tier, "total_count": count.total_count, "available_count": count.available_count, "total_purchased": count.total_purchased} for count in counts]
    return jsonify(counts_data), 200

@ticket_bp.route('/event_ticket_counts/<int:event_id>/<tier>', methods=['GET'])
def get_event_ticket_count(event_id, tier):
    count = EventTicketCount.query.filter_by(event_id=event_id, tier=tier).first()
    if count:
        return jsonify({"event_id": count.event_id, "tier": count.tier, "total_count": count.total_count, "available_count": count.available_count, "total_purchased": count.total_purchased}), 200
    return jsonify({"message": "Ticket count not found"}), 404

@ticket_bp.route('/event_ticket_counts', methods=['POST'])
def create_event_ticket_count():
    data = request.get_json()
    new_count = EventTicketCount(
        event_id=data.get('event_id'),
        tier=data.get('tier'),
        total_count=data.get('total_count'),
        available_count=data.get('available_count')
    )
    db.session.add(new_count)
    db.session.commit()
    return jsonify({"message": "Event ticket count created successfully!"}), 201

# Routes for EventTicketType
@ticket_bp.route('/event_ticket_types', methods=['GET'])
def get_event_ticket_types():
    types = EventTicketType.query.all()
    types_data = [{"id": type.id, "event_id": type.event_id, "tier_name": type.tier_name, "price": type.price} for type in types]
    return jsonify(types_data), 200

@ticket_bp.route('/event_ticket_types/<int:id>', methods=['GET'])
def get_event_ticket_type(id):
    ticket_type = EventTicketType.query.get(id)
    if ticket_type:
        return jsonify({"id": ticket_type.id, "event_id": ticket_type.event_id, "tier_name": ticket_type.tier_name, "price": ticket_type.price}), 200
    return jsonify({"message": "Ticket type not found"}), 404

@ticket_bp.route('/event_ticket_types', methods=['POST'])
def create_event_ticket_type():
    data = request.get_json()
    new_ticket_type = EventTicketType(
        event_id=data.get('event_id'),
        tier_name=data.get('tier_name'),
        price=data.get('price')
    )
    db.session.add(new_ticket_type)
    db.session.commit()
    return jsonify({"message": "Event ticket type created successfully!"}), 201