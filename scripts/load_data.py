"""
Loading the  CSV Data to SQLite Database
"""

import sqlite3
import pandas as pd
import os

print("Loading data into SQLite...")

# Connect to database (creates it if doesn't exist)
conn = sqlite3.connect('llm_analytics.db')

# Load users
print("Loading users...")
users = pd.read_csv('data/raw/users.csv')
users.to_sql('users', conn, if_exists='replace', index=False)
print(f"✓ Loaded {len(users):,} users")

# Load subscriptions
print("Loading subscriptions...")
subs = pd.read_csv('data/raw/subscriptions.csv')
subs.to_sql('subscriptions', conn, if_exists='replace', index=False)
print(f"✓ Loaded {len(subs):,} subscriptions")

# Load events (first chunk)
print("Loading events...")
events = pd.read_csv('data/raw/usage_events_part01.csv')
events.to_sql('usage_events', conn, if_exists='replace', index=False)
print(f"✓ Loaded {len(events):,} events")

conn.close()
print("\n Database created: llm_analytics.db")