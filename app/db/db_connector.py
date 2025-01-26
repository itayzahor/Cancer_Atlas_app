import mysql.connector

def get_db_connection():
    # Establishing the connection
    conn = mysql.connector.connect(
        host="localhost",        # Replace with your host
        user="root",    # Replace with your username
        password="Itay123456",# Replace with your password
        database="cancer_atlas" # Replace with your database name
    )
    print("Connection successful!")

    cursor = conn.cursor(dictionary=True)
    return conn, cursor

def execute_query(query_function, *args, **kwargs):
    """
    A generic function to execute a query and fetch results.

    Args:
        query_function (function): A query function from queries.py.
        *args: Positional arguments for the query function.
        **kwargs: Keyword arguments for the query function.

    Returns:
        list or dict: Query results.
    """
    conn, cursor = None, None
    try:
        conn, cursor = get_db_connection()
        # Execute the query
        query = query_function(*args, **kwargs)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Database query error: {e}")
        # Return None if there was an error
        return None
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
