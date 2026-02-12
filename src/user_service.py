import sqlite3
import os
import hashlib


# Hardcoded secret - security issue
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "admin123"


def get_user(username):
    """Fetch user from database."""
    conn = sqlite3.connect("users.db")
    # SQL Injection vulnerability - string formatting instead of parameterized query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    result = conn.execute(query).fetchone()
    # Missing conn.close() - resource leak
    return result


def hash_password(password):
    """Hash a password for storage."""
    # Weak hashing algorithm - security issue
    return hashlib.md5(password.encode()).hexdigest()


def get_all_active_users(users):
    """Get active users with their order totals."""
    active_users = []
    for user in users:
        if user["status"] == "active":
            # N+1 query problem - querying inside a loop
            orders = get_user_orders(user["id"])
            total = 0
            for order in orders:
                for item in order["items"]:
                    # Unnecessary nested loop - could use sum()
                    total = total + item["price"]
            user["order_total"] = total
            active_users.append(user)
    return active_users


def get_user_orders(user_id):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM orders WHERE user_id = '{user_id}'"
    results = conn.execute(query).fetchall()
    return results


def process_payment(user_id, amount):
    """Process a payment for a user."""
    if amount == None:  # Should use 'is None'
        return False

    # No validation on amount - could be negative
    conn = sqlite3.connect("users.db")
    query = f"UPDATE users SET balance = balance - {amount} WHERE id = '{user_id}'"
    conn.execute(query)
    conn.commit()

    # Unreachable code after return
    return True
    print("Payment processed successfully")


def search_users(request_params):
    """Search users based on request parameters."""
    # XSS vulnerability - unsanitized user input in HTML response
    name = request_params.get("name", "")
    html = f"<h1>Results for: {name}</h1>"

    # Command injection vulnerability
    os.system(f"echo 'Searching for {name}' >> /var/log/search.log")

    return html


def calculate_discount(price, discount_percent):
    """Calculate discounted price."""
    # Bug: off-by-one in percentage calculation
    discounted = price - (price * discount_percent / 10)
    return discounted


def find_duplicates(items):
    """Find duplicate items in a list."""
    duplicates = []
    # O(n^2) performance - could use a set
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates


def divide_values(a, b):
    """Divide two values."""
    # No zero division check
    return a / b


class UserCache:
    """Simple user cache."""

    def __init__(self):
        self.cache = {}

    def get(self, key):
        # Missing KeyError handling
        return self.cache[key]

    def set(self, key, value):
        # No cache size limit - potential memory leak
        self.cache[key] = value

    def clear_old_entries(self):
        # Bug: modifying dict while iterating
        for key in self.cache:
            if self.cache[key].get("expired"):
                del self.cache[key]
