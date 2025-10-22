import sqlite3
import hashlib
from datetime import datetime
from contextlib import contextmanager
import logging
import os

logger = logging.getLogger(__name__)

class SecureDatabase:
    def __init__(self, db_path="auth_database.db", encryption_key=None):
        """
        Initialize the database. If encryption_key is provided, attempts to use SQLCipher.
        """
        self.db_path = db_path
        self.encryption_key = encryption_key or os.getenv("DB_ENCRYPTION_KEY")
        self._init_db()

    def _get_connection(self):
        """Context manager for database connections with optional SQLCipher encryption"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        if self.encryption_key:
            try:
                conn.execute(f"PRAGMA key='{self.encryption_key}';")
            except sqlite3.OperationalError:
                logger.warning("SQLCipher not available — running without encryption.")
        return conn

    def _init_db(self):
        """Initialize database with required tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT,
                    name TEXT,
                    google_id TEXT UNIQUE,
                    provider TEXT DEFAULT 'email',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auth_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_hash TEXT NOT NULL,
                    event TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id)')
            conn.commit()
            logger.info("Database initialized successfully")

    @contextmanager
    def connection(self):
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def get_user_by_email(self, email: str):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create_user(self, email: str, hashed_password: str = None, **kwargs):
        provider = "google" if kwargs.get('google_id') else "email"
        name = kwargs.get('name')
        google_id = kwargs.get('google_id')
        with self.connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO users (email, hashed_password, name, google_id, provider)
                    VALUES (?, ?, ?, ?, ?)
                ''', (email, hashed_password, name, google_id, provider))
                user_id = cur.lastrowid
                cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                return dict(cur.fetchone())
            except sqlite3.IntegrityError as e:
                if "email" in str(e):
                    raise ValueError("Email already exists")
                elif "google_id" in str(e):
                    raise ValueError("Google ID already exists")
                raise

    def get_user_by_id(self, user_id: int):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_user_by_google_id(self, google_id: str):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all_users(self):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users ORDER BY id')
            return [dict(r) for r in cur.fetchall()]

    def delete_user(self, user_id: int):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM users WHERE id = ?', (user_id,))
            return cur.rowcount > 0

    def update_user(self, user_id: int, **kwargs):
        """Secure update using parameterized queries"""
        allowed_fields = ['email', 'hashed_password', 'name', 'google_id', 'provider']
        fields = [(k, v) for k, v in kwargs.items() if k in allowed_fields and v is not None]
        if not fields:
            return None

        set_clause = ", ".join(f"{k} = ?" for k, _ in fields)
        values = [v for _, v in fields] + [user_id]

        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(f'UPDATE users SET {set_clause} WHERE id = ?', values)
            if cur.rowcount > 0:
                return self.get_user_by_id(user_id)
            return None


class SecureAnalytics:
    def __init__(self, db_path="auth_database.db", encryption_key=None):
        self.db_path = db_path
        self.encryption_key = encryption_key

    def _hash_app_id(self, app_id: str) -> str:
        """Anonymize app_id using SHA-256 to avoid leaking identifiable info"""
        return hashlib.sha256(app_id.encode()).hexdigest()

    def track(self, app_id: str, event_type: str):
        """Track anonymized authentication events"""
        app_hash = self._hash_app_id(app_id)
        db = SecureDatabase(self.db_path, self.encryption_key)
        with db.connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO auth_events (app_hash, event, timestamp)
                VALUES (?, ?, ?)
            ''', (app_hash, event_type, datetime.utcnow().isoformat()))

    def get_events(self, app_id: str = None, limit: int = 100):
        """Retrieve authentication events (filtered by app_id if given)"""
        db = SecureDatabase(self.db_path, self.encryption_key)
        with db.connection() as conn:
            cur = conn.cursor()
            if app_id:
                cur.execute('''
                    SELECT * FROM auth_events
                    WHERE app_hash = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (self._hash_app_id(app_id), limit))
            else:
                cur.execute('''
                    SELECT * FROM auth_events
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            return [dict(row) for row in cur.fetchall()]


db = SecureDatabase()
analytics = SecureAnalytics()
