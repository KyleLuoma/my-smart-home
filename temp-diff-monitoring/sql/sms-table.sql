create table if not exists sms_log(
    timestamp datetime,
    phone_number text,
    message text
)