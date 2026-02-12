import sqlite3
import hashlib
import logging
from collections import Counter
from html import escape

logger = logging.getLogger(__name__)

DB_PATH = "users.db"
MAX_CACHE_SIZE = 1000


def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def get_user(username):
    """Fetch user from database."""
    conn = get_db_connection()
    try:
        query = "SELECT * FROM users WHERE username = ?"
        result = conn.execute(query, (username,)).fetchone()
        return result
    finally:
        conn.close()


def hash_password(password):
    """Hash a password for storage using SHA-256."""
    salt = hashlib.sha256(password.encode()).hexdigest()[:16]
    return hashlib.sha256((salt + password).encode()).hexdigest()


def get_user_orders(user_id):
    """Fetch orders for a given user."""
    conn = get_db_connection()
    try:
        query = "SELECT * FROM orders WHERE user_id = ?"
        results = conn.execute(query, (user_id,)).fetchall()
        return results
    finally:
        conn.close()


def get_all_active_users(users):
    """Get active users with their order totals."""
    active_users = []
    for user in users:
        if user["status"] == "active":
            orders = get_user_orders(user["id"])
            total = sum(
                item["price"]
                for order in orders
                for item in order["items"]
            )
            user["order_total"] = total
            active_users.append(user)
    return active_users


def process_payment(user_id, amount):
    """Process a payment for a user."""
    if amount is None:
        return False

    if amount <= 0:
        return False

    conn = get_db_connection()
    try:
        query = "UPDATE users SET balance = balance - ? WHERE id = ?"
        conn.execute(query, (amount, user_id))
        conn.commit()
        return True
    finally:
        conn.close()


def search_users(request_params):
    """Search users based on request parameters."""
    name = escape(request_params.get("name", ""))
    html = f"<h1>Results for: {name}</h1>"
    logger.info("Searching for %s", name)
    return html


def calculate_discount(price, discount_percent):
    """Calculate discounted price."""
    discounted = price - (price * discount_percent / 100)
    return discounted


def find_duplicates(items):
    """Find duplicate items in a list."""
    counts = Counter(items)
    return [item for item, count in counts.items() if count > 1]


def divide_values(a, b):
    """Divide two values."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class UserCache:
    """Simple user cache with size limit."""

    def __init__(self, max_size=MAX_CACHE_SIZE):
        self.cache = {}
        self.max_size = max_size

    def get(self, key):
        """Get a value from cache, returns None if not found."""
        return self.cache.get(key)

    def set(self, key, value):
        """Set a value in cache, evicts oldest entry if at capacity."""
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = value

    def clear_old_entries(self):
        """Remove expired entries from cache."""
        expired_keys = [
            key for key, value in self.cache.items()
            if value.get("expired")
        ]
        for key in expired_keys:
            del self.cache[key]
