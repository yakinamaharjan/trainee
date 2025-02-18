import mysql.connector

def db_connector(host: str, user: str, password: str, database: str) -> tuple:
        """
        Establish connection to database.
        
        Args:
            host (str): Hostname of database server.
            user (str): Username to connect to database.
            password (str): Password to connect to database.
            database (str): Name of database to connect to.
        
        Returns:
            conn (mysql.connector.connection.MySQLConnection): Connection object.
            cursor (mysql.connector.cursor.MySQLCursor): Cursor object.
        """
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = conn.cursor()
            print("Successfully connected to the database.")
            return conn, cursor
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            return None, None