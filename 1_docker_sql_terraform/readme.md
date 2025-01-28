## Docker Commands

### PostgreSQL Database Docker
```shell
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v /ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name=pg-database \
postgres:13
```

### pgAdmin Docker
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name=pg-admin \
dpage/pgadmin4
```

### test ingest data with python
```bash
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

### build docker
```bash
docker build -t taxi_ingest:0.1 .
```

### ingest yellow taxi data
```bash
docker run -it \
    --network=pg-network \
    taxi_ingest:0.1 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_data \
        --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

### ingest green taxi data
```bash
docker run -it \
    --network=1_docker_default \
    taxi_ingest:0.1 \
        --user=postgres \
        --password=postgres \
        --host=postgres \
        --port=5432 \
        --db=ny_taxi \
        --table_name=green_taxi_data \
        --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

### ingest zones data
```bash
docker run -it \
    --network=1_docker_default \
    taxi_ingest:0.1 \
        --user=postgres \
        --password=postgres \
        --host=postgres \
        --port=5432 \
        --db=ny_taxi \
        --table_name=zones \
        --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

## SQL Queries

### Trip Segmentation Count
```sql
select count(1) from green_taxi_data where trip_distance <= 1
select count(1) from green_taxi_data where trip_distance > 1 and trip_distance <= 3
select count(1) from green_taxi_data where trip_distance > 3 and trip_distance <= 7
select count(1) from green_taxi_data where trip_distance > 7 and trip_distance <= 10
select count(1) from green_taxi_data where trip_distance > 10
```

### Longest trip for each day
```sql
select
    date(lpep_pickup_datetime) AS pickup_date,
    max(trip_distance) as max_trip_distance
from
    green_taxi_data
group by
    pickup_date
order by
    max_trip_distance desc
```

### Three biggest pickup zones
```sql
select
    zpu."Zone" as pick_up_zone,
    sum(t.total_amount) as total_amount_sum
from
    green_taxi_data t
    join zones zpu on t."PULocationID" = zpu."LocationID"
where
    t.lpep_pickup_datetime::DATE = '2019-10-18'
group by
    zpu."Zone"
order by
    total_amount_sum desc
```

### Largest tip
```sql
select
    zdo."Zone" as drop_of_zone, t.tip_amount
from
    green_taxi_data t
    join zones zpu on t."PULocationID" = zpu."LocationID"
    join zones zdo on t."DOLocationID" = zdo."LocationID"
where
    zpu."Zone" = 'East Harlem North'
order by
    tip_amount desc
```
