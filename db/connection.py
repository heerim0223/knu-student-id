import pyodbc

def connect_db(path):
    return pyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"Dbq={path};"
    )