import oracledb
import pandas as pd

# Oracle DB credentials
USERNAME = "system"
PASSWORD = "123456789"
DSN = "localhost/XE"

def get_connection():
    return oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN)

def fetch_dataframe(query):
    conn = get_connection()
    df = pd.read_sql(query, con=conn)
    conn.close()
    return df

def add_publication(pub_id, title, summary, category, pub_type, pub_date,status):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("add_publication", [pub_id, title, summary, category, pub_type, pub_date])
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cur.close()
        conn.close()

def assign_author(pub_id, author_id, author_type):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("assign_author", [pub_id, author_id, author_type])
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cur.close()
        conn.close()
