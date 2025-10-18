class Database:
    def __init__(self):
        self.users = []
        self.sessions = {}
        self.next_id = 1

    def get_user_by_email(self, email: str):
        for user in self.users:
            if user["email"] == email:
                return user
        return None

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

    def get_user_by_id(self, user_id: int):
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None

    def get_user_by_google_id(self, google_id: str):
        for user in self.users:  # ← And this one
            if user.get("google_id") == google_id:
                return user
        return None

db = Database()
