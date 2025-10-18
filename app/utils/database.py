from typing import Dict, Optional

class Database:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.next_id = 1

    def create_user(self, email: str, hashed_password: str = None, **kwargs):
    user = {
        "id": self.next_id,
        "email": email,
        "hashed_password": hashed_password,
        "name": kwargs.get('name'),
        "google_id": kwargs.get('google_id'),
        "provider": "google" if kwargs.get('google_id') else "email"
    }
    self.users.append(user)
    self.next_id += 1
    return user

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        return self.users.get(user_id)

    def get_user_by_google_id(self, google_id: str):
        return next((user for user in self.users if user.get("google_id") == google_id), None)

db = Database()

