import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
    dbname="test1",
    user="default",
    password="ys2M1kEaZAPm",
    host="ep-white-wave-a432oopu-pooler.us-east-1.aws.neon.tech",
    port="5432"
    )
            
    return conn