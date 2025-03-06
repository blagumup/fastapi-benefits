import psycopg2
from config import get_settings

settings = get_settings()

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a synchronous connection to the database."""
        self.conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dbname=settings.DB_NAME
        )
        self.cursor = self.conn.cursor()
        print("✅ Connected to PostgreSQL")

    def disconnect(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("❌ Disconnected from PostgreSQL")

    def execute(self, query: str, *args):
        """Executes INSERT, UPDATE, DELETE queries."""
        self.cursor.execute(query, args)
        self.conn.commit()

    def fetch(self, query: str, *args):
        """Executes SELECT queries and returns results."""
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

# Singleton instance
db = Database()
