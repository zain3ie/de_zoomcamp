## SQL Queries

### Total Yellow Taxi rows in all 2020
```sql
select count(1) from de_zoomcamp.yellow_tripdata where filename like '%2020%'
```

### Total Green Taxi rows in all 2020
```sql
select count(1) from de_zoomcamp.green_tripdata where filename like '%2020%'
```

### Total Yellow Taxi rows in March 2021
```sql
select count(1) from de_zoomcamp.yellow_tripdata where filename like '%2021-03%'
```
