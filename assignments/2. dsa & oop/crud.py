# Write a CRUD program in python that can establish a connection to a SQL database (MySQL or MSSQL whichever one you are comfortable with) server given the username and password. Then write methods that can perform CRUD operations given proper arguments.

import mysql.connector
import csv
import pandas as pd
import os

class Database:
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
            q = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
            self.add_to_files("CREATE", q)
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
            for r in records:
                print(r)
        except mysql.connector.Error as e:
            print(f"Error fetching record: {e}")

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
            q = f"UPDATE users SET name = '{new_name}', email = '{new_email}' WHERE id = {id}"
            self.add_to_files("UPDATE", q)
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
            q = f"DELETE FROM users WHERE id = {id}"
            self.add_to_files("DELETE", q)
            self.cursor.execute(query, (id,))
            self.conn.commit()
            print("Record deleted successfully.")
        except mysql.connector.Error as e:
            print(f"Error deleting record: {e}")
    
    def add_to_files(self, qtype: str, query: str):
        """
        Exports queries to a csv and excel file.

        Args:
            qtype (str): Query type.
            query (str): Query to be executed.
        """
        try:
            data = {'Query Type': [qtype], 'Query': [query]}
            df = pd.DataFrame(data)
            df.to_csv('queries.csv', mode='a', index=False, header=False)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
        
        try:
            # df = pd.DataFrame([query])
            # df.to_excel("queries.xlsx", index=False)
            file = 'queries.xlsx'
            new_data = {'Query Type': [qtype], 'Query': [query]}
            df_new = pd.DataFrame(new_data)
            df_existing = pd.read_excel(file)
            df_combined = df_existing.append(df_new, ignore_index=True)
            df_combined.to_excel(file, index=False)
        except Exception as e:
            print(f"Error exporting data to Excel: {e}")


    def close_connection(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()
    
if __name__ == "__main__":
    db = Database(host="localhost", user="root", password="sdcdsFHS58%sd", database="python_crud")

    opt = 0
    while(opt != 4):
        os.system('cls')
        print()
        db.read_records()
        print("\n1. Create a record")
        print("2. Update a record")
        print("3. Delete a record")
        print("4. Exit")
        print("Enter your choice: ")
        opt = int(input())

        match opt:
            case 1:
                print("\nInsert Records:")
                print("Enter name: ")
                name = input()
                print("Enter email: ")
                email = input()
                db.create_record(name, email)
                input()
            case 2:
                print("\nUpdating a record:")
                print("Enter ID to update: ")
                id = int(input())
                print("Enter new name: ")
                name = input()  
                print("Enter new email: ")
                email = input()
                db.update_record(id, name, email)
                input()
            case 3:
                print("\nDeleting a record:")
                print("Enter ID to delete: ")
                id = int(input())
                db.delete_record(id)
                input()
            case 4:
                print("Exiting...")
                db.close_connection()
                break
    
