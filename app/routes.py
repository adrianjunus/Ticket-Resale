from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post, db
from .__init__ import render_markdown

# Create a Blueprint for the routes
main = Blueprint('main', __name__)

@main.route('/api/resale/offers', methods=['POST'])
def initiate_resale():
    data = request.json
    sale_id = str(uuid.uuid4())
    ticket = tickets.get(data['ticket_id'])

    if not ticket or ticket.locked:
        return jsonify({"error": "Ticket unavailable"}), 400

    buyer = users.get(data['buyer_email'])
    if not buyer:
        return jsonify({"error": "Buyer not found"}), 404

    ticket.locked = True
    resale = TicketResale(sale_id, ticket.ticket_id, ticket.owner_id, buyer['user_id'], data['price_cents'], 'initiated')

    # Create Stripe PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=data['price_cents'],
        currency='usd',
        metadata={'sale_id': sale_id}
    )
    resale.payment_intent_id = intent.id

    ticket_resales[sale_id] = resale
    return jsonify({"sale_id": sale_id, "stripe_client_secret": intent.client_secret})

@main.route('/api/resale/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        sale_id = intent['metadata']['sale_id']
        resale = ticket_resales.get(sale_id)

        if resale and resale.status == 'initiated':
            resale.status = 'paid'
            notifications.append({
                "to": resale.buyer_id,
                "message": f"Your payment was successful. Please confirm receipt of ticket '{tickets[resale.ticket_id].event_name}'."
            })

    return '', 200

@main.route('/api/resale/confirm/<sale_id>', methods=['POST'])
def confirm_ticket_receipt(sale_id):
    resale = ticket_resales.get(sale_id)
    if not resale or resale.status != 'paid':
        return jsonify({"error": "Sale not found or not ready for confirmation."}), 400

    resale.buyer_confirmed = True
    resale.status = 'completed'
    ticket = tickets[resale.ticket_id]
    ticket.owner_id = resale.buyer_id
    ticket.locked = False

    try:
        # Simulate payout using Stripe Transfer (requires Connect setup)
        transfer = stripe.Transfer.create(
            amount=resale.price_cents,  # Adjust amount for platform fee if needed
            currency="usd",
            destination="acct_seller_stripe_id_placeholder",  # Replace with seller's Stripe Connect account ID
            metadata={"sale_id": sale_id}
        )
        payout_message = "Funds have been released to the seller."
    except Exception as e:
        payout_message = f"Failed to release funds: {str(e)}"

    notifications.append({
        "to": resale.seller_id,
        "message": f"Your ticket has been confirmed received by the buyer. {payout_message}"
    })
    notifications.append({
        "to": resale.buyer_id,
        "message": f"You are now the owner of ticket '{ticket.event_name}'."
    })

    return jsonify({"message": "Ticket confirmed and ownership transferred.", "payout_status": payout_message})

@main.route('/api/resale/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    user_notes = [n for n in notifications if n['to'] == user_id]
    return jsonify(user_notes)
