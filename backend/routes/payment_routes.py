# payment_routes.py
from .common_imports import *
from models.payment import Payment
from extensions import db

# Routes for Payments
@payment_bp.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    payments_data = [{"id": payment.id, "ticket_id": payment.ticket_id, "transaction_id": payment.transaction_id, "status": payment.status} for payment in payments]
    return jsonify(payments_data), 200

@payment_bp.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get(id)
    if payment:
        return jsonify({"id": payment.id, "ticket_id": payment.ticket_id, "transaction_id": payment.transaction_id, "status": payment.status}), 200
    return jsonify({"message": "Payment not found"}), 404

@payment_bp.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    new_payment = Payment(
        ticket_id=data.get('ticket_id'),
        transaction_id=data.get('transaction_id'),
        status=data.get('status')
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Payment created successfully!"}), 201

@payment_bp.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get(id)
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Payment deleted successfully!"}), 200
    return jsonify({"message": "Payment not found"}), 404