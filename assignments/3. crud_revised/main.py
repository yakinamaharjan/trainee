from db_manager import DatabaseManager
from export import ExportManager

if __name__ == "__main__":
    db = DatabaseManager(host="localhost", user="root", password="sdcdsFHS58%sd", database="python_crud")
    exporter = ExportManager()

    print("\nInsert Records:")
    name = input("Enter name: ")
    email = input("Enter email: ")
    db.create_record(name, email)
    exporter.export("INSERT", db.read_records())

    print("\nUpdating a record:")
    id = int(input("Enter ID to update: "))
    name = input("Enter new name: ")  
    email = input("Enter new email: ")
    db.update_record(id, name, email)
    exporter.export("UPDATE", db.read_records())

    print("\nDeleting a record:")
    id = int(input("Enter ID to delete: "))
    db.delete_record(id)
    exporter.export("DELETE", db.read_records())

    db.close_connection()
