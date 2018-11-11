import asyncio
import asyncpg


async def create_tables(database_uri):
    conn = await asyncpg.connect(database_uri)
    await conn.execute('''
        CREATE TABLE users(
            id SERIAL PRIMARY KEY,
            email VARCHAR(30) UNIQUE,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            created TIMESTAMP NOT NULL DEFAULT NOW(),
            is_active BOOL NOT NULL DEFAULT TRUE,
            api_key UUID DEFAULT uuid_generate_v4()
        );

        CREATE TABLE albums(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            metadata JSONB,
            created TIMESTAMP NOT NULL DEFAULT NOW(),
            updated TIMESTAMP NOT NULL DEFAULT NOW()
        );

        CREATE TABLE tracks(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            album_id INTEGER REFERENCES albums(id) ON DELETE CASCADE,
            created TIMESTAMP NOT NULL DEFAULT NOW(),
            updated TIMESTAMP NOT NULL DEFAULT NOW()
        );
    ''')

    await conn.close()


async def drop_tables(database_uri):
    conn = await asyncpg.connect(database_uri)
    await conn.execute("DROP TABLE users, albums, tracks;")
    await conn.close()


if __name__ == "__main__":
    database_uri = 'postgresql://user:password@host:port/database'
    asyncio.get_event_loop().run_until_complete(drop_tables(database_uri))
    asyncio.get_event_loop().run_until_complete(create_tables(database_uri))
