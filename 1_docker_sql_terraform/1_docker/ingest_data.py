import os
import argparse
import pandas as pd

from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'

    os.system(f'curl -L -o {csv_name} {url}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_csv(url)

    if 'lpep_pickup_datetime' in df.columns:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    if 'lpep_dropoff_datetime' in df.columns:
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    chunksize = 100000

    for i in range(0, len(df), chunksize):
        t_start = time()

        df[i:i+chunksize].to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end-t_start))

        os.remove(csv_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='insert csv data to postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we write the result to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
