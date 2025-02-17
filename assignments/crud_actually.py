# Write a CRUD program in python that can establish a connection to a SQL database (MySQL or MSSQL whichever one you are comfortable with) server given the username and password. Then write methods that can perform CRUD operations given proper arguments.

import mysql.connector
import csv
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Establish connection to database.
        
        Args:
            host (str): Hostname of database server.
            user (str): Username to connect to database.
            password (str): Password to connect to database.
            database (str): Name of database to connect to.
        """
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("Successfully connected to the database.")
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")

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
    
    def export(self, qr: str):
        """
        Exports all records to a csv file and a excel file.
        """
        cfile = './files/queries.csv'
        xfile = './files/queries.xlsx'
        data = self.read_records()
        q = pd.DataFrame([[qr] + [''] * (len(data[0]) - 1)]) if data else pd.DataFrame([[qr]])
        df = pd.DataFrame(data)

        try:
            q.to_csv(cfile, mode='a', index=False, header=False)
            df.to_csv(cfile, mode='a', index=False, header=False)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
        
        try:
            if os.path.exists(xfile): 
                df_existing = pd.read_excel(xfile, header=None)
                df_combined = pd.concat([df_existing, q, df], ignore_index=True)
            else:
                df_combined = pd.concat([q, df], ignore_index=True)

            df_combined.to_excel(xfile, index=False, header=False)
        except Exception as e:
            print(f"Error exporting data to Excel: {e}")


    def close_connection(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()
    
if __name__ == "__main__":
    db = DatabaseManager(host="localhost", user="root", password="sdcdsFHS58%sd", database="python_crud")

    print("\nInsert Records:")
    print("Enter name: ")
    name = input()
    print("Enter email: ")
    email = input()
    db.create_record(name, email)
    db.export("INSERT")
    # print("\nAll records:")
    # db.print_records()

    print("\nUpdating a record:")
    print("Enter ID to update: ")
    id = int(input())
    print("Enter new name: ")
    name = input()  
    print("Enter new email: ")
    email = input()
    db.update_record(id, name, email)
    db.export("UPDATE")
    # print("\nUpdated database:")
    # db.print_records()
    
    print("\nDeleting a record:")
    print("Enter ID to delete: ")
    id = int(input())
    db.delete_record(id)
    db.export("DELETE")
    # print("\nUpdated database:")
    # db.print_records()

    db.close_connection()

