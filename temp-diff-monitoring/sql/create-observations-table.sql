create table if not exists observations(
    timestamp DATETIME,
    station_ip TEXT,
    temp_f FLOAT,
    humidity FLOAT
);

