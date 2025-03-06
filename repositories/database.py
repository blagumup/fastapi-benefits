import asyncpg
from config import get_settings

settings = get_settings()

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Establishes a connection pool to the database."""
        self.pool = await asyncpg.create_pool(
            dsn=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )

    async def disconnect(self):
        """Closes the database connection."""
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args):
        """Executes a query without returning data (INSERT, UPDATE, DELETE)."""
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        """Executes a query and returns results (SELECT)."""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

# Singleton instance
db = Database()
