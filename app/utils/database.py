from typing import Dict, Optional

class Database:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.next_id = 1

    def create_user(self, email: str, hashed_password: str) -> Dict:
        user_id = self.next_id
        user = {
            "id": user_id,
            "email": email,
            "hashed_password": hashed_password,
            "created_at": "2025-10-18" 
        }
        self.users[user_id] = user
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
