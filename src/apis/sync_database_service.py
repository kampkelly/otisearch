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

    async def get_schema_info(self):
        '''
        Returns the list of all tables, their columns with types, and relationships (one level deep)
        '''
        await self.setup()
        if not self.pool:
            raise Exception("Database connection not initialized. Call setup() first.")

        async with self.pool.acquire() as connection:
            # Query to get tables, columns, and their types
            schema_query = """
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default
            FROM 
                information_schema.tables t
            JOIN 
                information_schema.columns c ON t.table_name = c.table_name
            WHERE 
                t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
            ORDER BY 
                t.table_name, c.ordinal_position;
            """
            
            # Query to get foreign key relationships
            fk_query = """
            SELECT
                tc.table_name, kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM 
                information_schema.table_constraints AS tc 
            JOIN 
                information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN 
                information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE 
                tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public';
            """
            
            schema_rows = await connection.fetch(schema_query)
            fk_rows = await connection.fetch(fk_query)

        # Process the results
        schema_info = {}
        for row in schema_rows:
            table_name = row['table_name']
            if table_name not in schema_info:
                schema_info[table_name] = {'columns': [], 'relationships': []}
            
            schema_info[table_name]['columns'].append({
                'name': row['column_name'],
                'type': row['data_type'],
                'nullable': row['is_nullable'],
                'default': row['column_default']
            })

        # Add relationship information
        for row in fk_rows:
            table_name = row['table_name']
            if table_name in schema_info:
                schema_info[table_name]['relationships'].append({
                    'column': row['column_name'],
                    'foreign_table': row['foreign_table_name'],
                    'foreign_column': row['foreign_column_name'],
                    'columns': schema_info[row['foreign_table_name']]['columns'] if row['foreign_table_name'] in schema_info else []
                })

        return schema_info