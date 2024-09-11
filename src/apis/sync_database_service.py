import asyncpg
import asyncio


class SyncDatabaseConnection:
    def __init__(self, connection_string: str, min_size=1, max_size=5):
        self.connection_string = connection_string
        self.conn = None
        self.min_size = min_size
        self.max_size = max_size
        self.pool = None
        self.initialized = True

    async def setup(self):
        '''
        Initializes the database connection pool
        '''
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.connection_string,
                min_size=self.min_size, max_size=self.max_size
            )
            # todo: pull in default max_pools with SHOW max_connections;
            print('Connection Succeded!')
        except Exception as error:
            raise error
 
    async def close(self):
        '''
        Closes the connection pool
        '''
        if self.pool:
            await self.pool.close()

    async def get_tables(self):
        '''
        Returns the list of all tables in the database
        '''
        await self.setup()
        if not self.pool:
            raise Exception("Database connection not initialized. Call setup() first.")

        async with self.pool.acquire() as connection:
            query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
            rows = await connection.fetch(query)
            return [row['table_name'] for row in rows]

    async def get_columns(self, table_name: str):
        '''
        Returns the list of all columns in the specified table
        '''
        await self.setup()
        if not self.pool:
            raise Exception("Database connection not initialized. Call setup() first.")

        async with self.pool.acquire() as connection:
            query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            """
            rows = await connection.fetch(query, table_name)
            return [row['column_name'] for row in rows]
