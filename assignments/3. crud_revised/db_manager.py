import os
import pandas as pd
from db_conn import db_connector

class DatabaseManager:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn, self.cursor = db_connector(host, user, password, database)
    
    def create_record(self, name: str, email: str):
        """
        Inserts a new user record.

        Args:
            name (str): Name of new user.
            email (str): Email of new user.
        """
        try:
            query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            self.cursor.execute(query, (name, email))
            self.conn.commit()
            print("Record added successfully.")
        except mysql.connector.Error as e:
            print(f"Error adding record: {e}")

    def read_records(self) -> list:
        """
        Fetches all records from the database.

        Returns:
            list: List of all records from the database.
        """
        query = "SELECT * FROM users"
        try:
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            print(f"Error fetching record: {e}")
            

    def print_records(self):
        """
        Prints all records from the database.
        """
        records = self.read_records()
        if not records:
            print("No records found.")
            return
        for r in records:
            print(r)

    def update_record(self, id: int, new_name: str, new_email: str):
        """
        Updates an existing user record.

        Args:
            id (int): ID of the user to update.
            new_name (str): New name of the user.
            new_email (str): New email of the user.
        """
        try:
            query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
            self.cursor.execute(query, (new_name, new_email, id))
            self.conn.commit()
            print("Record updated successfully.")
        except mysql.connector.Error as e:
            print(f"Error updating record: {e}")

    def delete_record(self, id: int):
        """
        Deletes a user record by ID.

        Args:
            id (int): ID of the user to be deleted.
        """
        try:
            query = "DELETE FROM users WHERE id = %s"
            self.cursor.execute(query, (id,))
            self.conn.commit()
            print("Record deleted successfully.")
        except mysql.connector.Error as e:
            print(f"Error deleting record: {e}")

    def close_connection(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()
