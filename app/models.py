# app/models.py

class Ticket:
    def __init__(self, ticket_id, event_name, owner_id):
        self.ticket_id = ticket_id
        self.event_name = event_name
        self.owner_id = owner_id
        self.locked = False

class TicketResale:
    def __init__(self, sale_id, ticket_id, seller_id, buyer_id, price_cents, status):
        self.sale_id = sale_id
        self.ticket_id = ticket_id
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.price_cents = price_cents
        self.status = status
        self.created_at = datetime.utcnow()
        self.payment_intent_id = None
        self.buyer_confirmed = False
