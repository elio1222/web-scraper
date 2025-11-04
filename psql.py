import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host="localhost", dbname = "csc363project", user = "postgres", password = os.getenv("password"), port = 5432)

cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS Department (
            DEPT_NAME VARCHAR(30) PRIMARY KEY,
            SCHOOL_NAME VARCHAR(100)
            );
""")

cur.execute("""
INSERT INTO Department
            VALUES('Computer Science', 'School of Engineering, Physics, & Computing');
""")

cur.execute("""
SELECT * FROM Department;
""")

result = cur.fetchone()
print(result)



conn.commit()

cur.close()
conn.close()