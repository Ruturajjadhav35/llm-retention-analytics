import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('llm_analytics.db')

print("=" * 70)
print("LLM PLATFORM RETENTION ANALYSIS")
print("=" * 70)
print()

# ============================================
# QUERY 1: User Segment Distribution
# ============================================

print("QUERY 1: User Segment Distribution")
print("-" * 70)

query1 = """
SELECT 
    user_segment,
    COUNT(*) as user_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as percentage
FROM users
GROUP BY user_segment
ORDER BY user_count DESC
"""

df1 = pd.read_sql_query(query1, conn)
print(df1.to_string(index=False))
print()

# ============================================
# QUERY 2: Top Event Types
# ============================================

print("QUERY 2: Top Event Types")
print("-" * 70)

query2 = """
SELECT 
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM usage_events), 2) as percentage
FROM usage_events
GROUP BY event_type
ORDER BY event_count DESC
"""

df2 = pd.read_sql_query(query2, conn)
print(df2.to_string(index=False))
print()

# ============================================
# QUERY 3: Feature Adoption
# ============================================

print("QUERY 3: Feature Adoption Rates")
print("-" * 70)

query3 = """
SELECT 
    feature_used,
    COUNT(DISTINCT user_id) as users_using_feature,
    ROUND(COUNT(DISTINCT user_id) * 100.0 / (SELECT COUNT(DISTINCT user_id) FROM usage_events), 2) as adoption_rate
FROM usage_events
GROUP BY feature_used
ORDER BY adoption_rate DESC
"""

df3 = pd.read_sql_query(query3, conn)
print(df3.to_string(index=False))
print()

# ============================================
# QUERY 4: 30-Day Retention Rate
# ============================================

print("QUERY 4: 30-Day Retention Rate")
print("-" * 70)

query4 = """
WITH user_activity AS (
    SELECT 
        u.user_id,
        u.signup_date,
        u.user_segment,
        MAX(CASE 
            WHEN julianday(e.event_date) > julianday(u.signup_date) + 30
            THEN 1 ELSE 0 
        END) as active_after_30
    FROM users u
    LEFT JOIN usage_events e ON u.user_id = e.user_id
    WHERE julianday(date('now')) - julianday(u.signup_date) >= 30
    GROUP BY u.user_id, u.signup_date, u.user_segment
)
SELECT 
    user_segment,
    COUNT(*) as total_users,
    SUM(active_after_30) as retained_users,
    ROUND(100.0 * SUM(active_after_30) / COUNT(*), 2) as retention_rate
FROM user_activity
GROUP BY user_segment
ORDER BY retention_rate DESC
"""

df4 = pd.read_sql_query(query4, conn)
print(df4.to_string(index=False))
print()

# ============================================
# QUERY 5: Conversion Rate (Free to Paid)
# ============================================

print("QUERY 5: Free to Paid Conversion")
print("-" * 70)

query5 = """
WITH user_plans AS (
    SELECT 
        u.user_id,
        u.initial_plan,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM subscriptions s 
                WHERE s.user_id = u.user_id 
                AND s.plan_type IN ('pro', 'enterprise')
            ) THEN 1 ELSE 0 
        END as has_upgraded
    FROM users u
    WHERE u.initial_plan = 'free'
)
SELECT 
    COUNT(*) as free_users,
    SUM(has_upgraded) as upgraded_users,
    ROUND(100.0 * SUM(has_upgraded) / COUNT(*), 2) as conversion_rate
FROM user_plans
"""

df5 = pd.read_sql_query(query5, conn)
print(df5.to_string(index=False))
print()

# ============================================
# EXPORT RESULTS
# ============================================

print("=" * 70)
print("EXPORTING RESULTS TO CSV")
print("=" * 70)
print()

# Create results directory if it doesn't exist
import os
os.makedirs('results', exist_ok=True)

# Export each result
df1.to_csv('results/user_segments.csv', index=False)
print("✓ Exported: results/user_segments.csv")

df2.to_csv('results/event_types.csv', index=False)
print("✓ Exported: results/event_types.csv")

df3.to_csv('results/feature_adoption.csv', index=False)
print("✓ Exported: results/feature_adoption.csv")

df4.to_csv('results/retention_by_segment.csv', index=False)
print("✓ Exported: results/retention_by_segment.csv")

df5.to_csv('results/conversion_rate.csv', index=False)
print("✓ Exported: results/conversion_rate.csv")

print()
print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print()
print(" Key Findings:")
print(f"  • Total Users: {len(pd.read_sql_query('SELECT * FROM users', conn)):,}")
print(f"  • Total Events: {len(pd.read_sql_query('SELECT * FROM usage_events', conn)):,}")
print(f"  • Highest Retention Segment: {df4.iloc[0]['user_segment']}")
print(f"  • Overall Conversion Rate: {df5.iloc[0]['conversion_rate']}%")
print()


conn.close()