## SQL Queries

### Create external table reffering to GCS path
```sql
CREATE OR REPLACE EXTERNAL TABLE de_zoomcamp.yellow_tripdata_2024_ext
OPTIONS (
  format = 'parquet',
  uris = ['gs://de-zoomcamp-449704/yellow_tripdata_2024-*.parquet']
);
```

### Create non partitioned table from external table
```sql
CREATE OR REPLACE TABLE de_zoomcamp.yellow_tripdata_2024_materialized AS
SELECT * FROM de_zoomcamp.yellow_tripdata_2024_ext;
```

### Count of records for the 2024 yellow taxi data
```sql
SELECT COUNT(1)
FROM de_zoomcamp.yellow_tripdata_2024_materialized;
```

### Count the distinct number of PULocationID for external table
```sql
SELECT COUNT(DISTINCT PULocationID)
FROM de_zoomcamp.yellow_tripdata_2024_ext;
```

### Count the distinct number of PULocationID for materialized table
```sql
SELECT COUNT(DISTINCT PULocationID)
FROM de_zoomcamp.yellow_tripdata_2024_materialized;
```

### Retrieve the PULocationID from materialized table
```sql
SELECT PULocationID
FROM de_zoomcamp.yellow_tripdata_2024_materialized;
```

### Retrieve the PULocationID and DOLocationID from materialized table
```sql
SELECT PULocationID, DOLocationID
FROM de_zoomcamp.yellow_tripdata_2024_materialized;
```

### Records have a fare_amount of 0
```sql
SELECT COUNT(1)
FROM de_zoomcamp.yellow_tripdata_2024_materialized WHERE fare_amount = 0;
```

### Create partisioned table from external table
```sql
CREATE OR REPLACE TABLE de_zoomcamp.yellow_tripdata_2024_partisioned
PARTITION BY DATE(tpep_dropoff_datetime) AS
SELECT * FROM de_zoomcamp.yellow_tripdata_2024_ext;
```

### Create partisioned and clustered table from external table
```sql
CREATE OR REPLACE TABLE de_zoomcamp.yellow_tripdata_2024_partisioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM de_zoomcamp.yellow_tripdata_2024_ext;
```

### Retrieve the distinct VendorID between tpep_dropoff_datetime for materialized table
```sql
SELECT COUNT(DISTINCT VendorID)
FROM de_zoomcamp.yellow_tripdata_2024_materialized
WHERE DATE(tpep_dropoff_datetime) >= '2024-03-01' AND DATE(tpep_dropoff_datetime) <= '2024-03-15';
```

### retrieve the distinct VendorID between tpep_dropoff_datetime for partisioned and clustered table
```sql
SELECT COUNT(DISTINCT VendorID)
FROM de_zoomcamp.yellow_tripdata_2024_partisioned_clustered
WHERE DATE(tpep_dropoff_datetime) >= '2024-03-01' AND DATE(tpep_dropoff_datetime) <= '2024-03-15';
```
