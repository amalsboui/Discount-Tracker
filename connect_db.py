from database import get_connection

conn = get_connection()
print("Connection successful!" if conn else "Connection failed.")
conn.close()
