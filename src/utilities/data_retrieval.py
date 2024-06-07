from utilities.constants import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    VECTOR_DB_NAME,
)
import psycopg2
import psycopg2.extras


def connect_vector_db():
    """
    Connect to the database.

    Returns:
        tuple: A tuple containing the connection and cursor objects.
    """
    # Connect to the postgres DB
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=VECTOR_DB_NAME,
    )

    # Open a cursor to perform database operations
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return conn, cur


def get_offset(filename: str):
    offset = 0
    with open(filename, "r") as file:
        offset = file.readline()
    return int(offset)


def update_offset(filename: str, offset: str):
    if offset:
        with open(filename, "w") as file:
            file.write(offset)


def check_data(table_name, video_id):

    conn, cur = connect_vector_db()

    cur = conn.cursor()

    # Query the database to see if the ID exists
    query = (
        f"SELECT EXISTS(SELECT * FROM {table_name} WHERE metadata_ ->> 'video_id' = %s)"
    )
    cur.execute(query, (video_id,))

    result = cur.fetchone()[0]
    # Fetch the result
    cur.close()
    conn.close()

    return result


def retrieve_metadata(table_name):
    result = []
    conn, cur = connect_vector_db()

    cur = conn.cursor()

    # Query the database to see if the ID exists
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    records = cur.fetchall()
    for record in records:
        result.append(record)
    cur.close()
    conn.close()

    return result


def insert_data(records, table_name, url_template):
    """
    Insert records into the specified table.

    Args:
        records (list): A list of records to be inserted.
        table_name (str): The name of the table to insert the records into.

    Returns:
        None
    """
    # Connect to the database
    connection, cursor = connect_db()
    # Prepare the SQL query
    query = f"""
    INSERT INTO {table_name} (video_id, video_url, video_text)
    VALUES (%s, %s, %s)
    """

    # Execute the query for each record
    for record in records:
        values = (
            record.id_,
            url_template + record.id_,
            record.text,
        )
        cursor.execute(query, values)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()


def retrieve_data(table: str, columns: list, video_id: str):
    result = []
    conn, cur = connect_db()
    selected_columns = ",".join(columns) if columns else "*"
    # Execute a query
    statement = f"SELECT {selected_columns} FROM {table} WHERE video_id = %s"

    cur.execute(statement, (video_id,))

    records = cur.fetchall()
    for record in records:
        result.append(record["video_text"])

    # Don't forget to close the connection
    cur.close()
    conn.close()

    return result
