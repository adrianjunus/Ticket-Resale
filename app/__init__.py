# Ticket Resale P2P Platform - Flask Backend Scaffold

from flask import Flask, request, jsonify
import stripe
import uuid
from .models import Ticket
from datetime import datetime, timedelta

app = Flask(__name__)

# === Configuration ===
stripe.api_key = 'sk_test_...'
endpoint_secret = 'whsec_...'

# Simulated in-memory storage (replace with DB in production)
tickets = {}
users = {}
ticket_resales = {}
notifications = []

# === Simulated Data ===
users['alice@example.com'] = {"user_id": "u1", "email": "alice@example.com"}
users['bob@example.com'] = {"user_id": "u2", "email": "bob@example.com"}
tickets['t1'] = Ticket(ticket_id='t1', event_name='Indie Fest 2025', owner_id='u1')

# === Run Server ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
