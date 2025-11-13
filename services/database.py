import asyncpg
from contextlib import asynccontextmanager
from config import config

class Database:
    """Handle database operations"""

    def __init__(self):
        self.conn_params = {
            "host": config.DB_HOST,
            "port": config.DB_PORT,
            "database": config.DB_NAME,
            "user": config.DB_USER,
            "password": config.DB_PASSWORD
        }

    @asynccontextmanager
    async def get_connection(self):
        """context manager for database connection"""
        conn = await asyncpg.connect(**self.conn_params)
        try:
            yield conn
        finally:
            await conn.close()

    async def search_by_embedding(self, embedding, limit=1, threshold=0.7):
        embedding_str = '[' + ','.join(map(str, embedding)) + ']'
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT id,
                       1 - (image_embedding <=> $1::vector) AS similarity
                FROM toothpastes
                WHERE image_embedding IS NOT NULL
                  AND 1 - (image_embedding <=> $1::vector) >= $2
                ORDER BY image_embedding <=> $1::vector
                LIMIT $3
            """, embedding_str, threshold, limit)
        return [dict(row) for row in rows]
