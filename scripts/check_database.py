import sqlite3

conn = sqlite3.connect('llm_analytics.db')
cursor = conn.cursor()

# Check what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(f"  • {table[0]}")
    
    # Count rows in each table
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"    Rows: {count:,}")
    print()

conn.close()