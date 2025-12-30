import psycopg2

def connect_to_db():
    print("Connecting to the PostgreSQL database...")

    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5000",
            dbname="db",
            user="db_user",
            password="db_password"
        )
        print("Database connection successful.")
        return conn

    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise


def create_table(conn):
    print("Creating schema and table if they do not exist...")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;

            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        cursor.close()
        print("Schema and table created successfully.")

    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        conn.rollback()
        raise


if __name__ == "__main__":
    conn = connect_to_db()
    create_table(conn)
    conn.close()
