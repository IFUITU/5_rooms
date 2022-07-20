import psycopg2
from config import config


""" Connect to the PostgreSQL database server """
conn = None
try:
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
