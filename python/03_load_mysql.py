import pandas as pd
import mysql.connector

# ============================================================
# 1. LOAD CLEAN CSV
# ============================================================

file_path = "../data/processed/social_media_clean.csv"

df = pd.read_csv(file_path)

print("CSV loaded successfully")
print("Rows:", len(df))


# ============================================================
# 2. CONNECT TO MYSQL
# ============================================================

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="mysqlbysiya",
    database="social_media_analysis"
)

cursor = connection.cursor()

print("Connected to MySQL successfully")


# ============================================================
# 3. INSERT DATA
# ============================================================

insert_query = """
INSERT INTO social_media_posts (
    post_id,
    platform,
    content_type,
    topic,
    language,
    region,
    post_datetime,
    hashtags,
    sentiment_score,
    views,
    likes,
    comments,
    shares,
    engagement_rate,
    is_viral,
    total_engagement,
    engagement_per_1000_views,
    like_rate,
    comment_rate,
    share_rate,
    post_date,
    year,
    month,
    month_name,
    day_of_week,
    post_hour,
    calculated_engagement_rate,
    engagement_rate_difference
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s
)
"""


# ============================================================
# 4. PREPARE DATA
# ============================================================

data = df.where(pd.notnull(df), None)

rows = [
    tuple(row)
    for row in data.itertuples(index=False, name=None)
]


# ============================================================
# 5. INSERT INTO MYSQL
# ============================================================

cursor.executemany(
    insert_query,
    rows
)

connection.commit()

print("Data inserted successfully!")
print("Rows inserted:", cursor.rowcount)


# ============================================================
# 6. CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("MySQL connection closed.")