class Config:
    API_BASE_URL = 'http://localhost:5000'
    AUTH_LOGIN_URL = f'{API_BASE_URL}/auth/login'
    AUTH_USERS_URL = f'{API_BASE_URL}/auth/users'
    DATABASE_NAME = 'banco.db'