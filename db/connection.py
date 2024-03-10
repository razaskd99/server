import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
    dbname="verceldb",
    user="default",
    password="RNkArZ4sfh9H",
    host="ep-aged-dream-a41ao23e-pooler.us-east-1.aws.neon.tech",
    port="5432"
    )
            
    return conn


