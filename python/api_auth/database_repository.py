import sqlite3
import bcrypt
import secrets

class DatabaseRepository:
    def __init__(self, db_name='auth_system.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                )
            ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions(
                    user_id INTEGER NOT NULL,
                    token TEXT NOT NULL UNIQUE,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
        self.conn.commit()

    def create_user(self, username, password):
        if self.get_user_by_username(username):
            return None

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users(username, password_hash) VALUES (?, ?)
        ''', (username, hashed_password.decode('utf-8')))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE username = ?
        ''', (username,))
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'username': user[1], 'password_hash': user[2]}
        return None

    def check_password(self, username, password):
        user = self.get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
        return None

    def create_session(self, user_id):
        token = secrets.token_hex(16)
        cursor = self.conn.cursor()
        cursor.execute('''
                INSERT INTO sessions (user_id, token) VALUES (?, ?)
            ''', (user_id, token))
        self.conn.commit()
        return token

    def get_user_by_token(self, token):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_id FROM sessions WHERE token = ?
        ''', (token,))
        session = cursor.fetchone()
        if not session:
            return None

        user_id = session[0]
        cursor.execute('''
                SELECT * FROM users WHERE id = ?
            ''', (user_id,))
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'username': user[1]}
        return None

    def update_username(self, user_id, new_username):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
                DELETE FROM sessions WHERE user_id = ?
            ''', (user_id,))
        cursor.execute('''
                DELETE FROM users WHERE id = ?
            ''', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
