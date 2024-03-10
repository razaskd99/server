import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
    dbname="verceldb",
    user="default",
    password="3yHMjDYeZ0VO",
    host="ep-bitter-heart-a4t4x9yx-pooler.us-east-1.aws.neon.tech",
    port="5432"
    )
            
    return conn