import psycopg2 as pgsql

# Database connection details
DB_CONFIG = {
    "database": "library",
    "user": "postgres",
    "password": "Harsh@1405",
    "host": "localhost",
    "port": "5432"
}

def get_connection() :
    return pgsql.connect(**DB_CONFIG)

def initial_table_creation() :
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL UNIQUE,
            author VARCHAR(50) NOT NULL,
            available BOOLEAN DEFAULT TRUE
        );
    """)

    curr.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact VARCHAR(15) NOT NULL UNIQUE
        );
    """)

    curr.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            member_id INT NOT NULL,
            book_id INT NOT NULL,
            issue_date DATE NOT NULL DEFAULT CURRENT_DATE,
            return_date DATE,
            status VARCHAR(10) NOT NULL DEFAULT 'issued',
            CONSTRAINT fk_member FOREIGN KEY (member_id) REFERENCES members(member_id),
            CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES books(book_id)
        );
    """)
    
    conn.commit()
    curr.close()
    conn.close()

def query_execute(query, fetch = False) :
    try :
        conn = get_connection()
        curr = conn.cursor()

        curr.execute(query)

        result = None
        
        if fetch:
            result = curr.fetchall()

        conn.commit()
        curr.close()
        conn.close()
        return result

    except Exception as e :
        print("Some Error while interacting with database")
        print("Error : ", e)