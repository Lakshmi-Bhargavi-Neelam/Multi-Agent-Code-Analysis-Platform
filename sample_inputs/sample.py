# Standard library imports
import os
import json
import math

# Third-party import
import requests


# Class responsible for user authentication
class AuthService:
    # Constructor initializes API endpoint
    def __init__(self):
        self.api_url = "https://example.com/login"

    # Authenticates user against external API
    def authenticate(self, username, password):
        # Input validation
        if not username:
            raise ValueError("Username is required")

        if not password:
            raise ValueError("Password is required")

        # Prepare payload
        payload = {
            "username": username,
            "password": password
        }

        # External API request
        response = requests.post(self.api_url, json=payload)

        # Response handling
        if response.status_code == 200:
            data = response.json()

            if "token" in data:
                return data["token"]

            else:
                raise Exception("Authentication token missing")

        elif response.status_code == 401:
            raise Exception("Unauthorized access")

        else:
            raise Exception("Unexpected API response")


# Utility function to validate usernames
def validate_user(user):
    # Reject null user
    if user is None:
        return False

    # Reject too short usernames
    if len(user) < 3:
        return False

    return True


# Processes a list of users
def process_users(users):
    valid_users = []

    for user in users:
        if validate_user(user):
            valid_users.append(user)

    return valid_users


# Save processed data into local JSON file
def save_to_file(data):
    with open("output.json", "w") as f:
        json.dump(data, f)


# Mathematical helper utility
def calculate_discount(price, percentage):
    if percentage < 0 or percentage > 100:
        raise ValueError("Invalid discount percentage")

    discount_amount = (price * percentage) / 100
    return price - discount_amount


# Example function with nested complexity
def complex_business_logic(order_total, user_type, is_holiday):
    if order_total > 1000:
        if user_type == "premium":
            if is_holiday:
                return "30% Discount"
            else:
                return "20% Discount"
        else:
            if is_holiday:
                return "10% Discount"
            else:
                return "5% Discount"

    return "No Discount"


# Simple helper function
def helper():
    pass