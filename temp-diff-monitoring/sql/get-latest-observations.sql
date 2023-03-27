select observations.station_ip, location, timestamp, temp_f, humidity
from observations
    join stations on observations.station_ip = stations.station_ip
where timestamp in (
    select max(timestamp) from observations group by station_ip
    );
