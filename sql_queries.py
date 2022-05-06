import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_crm_table_drop = ("""
DROP TABLE IF EXISTS crm_stage
""")

staging_device_table_drop = ("""
DROP TABLE IF EXISTS dev_stage
""")

staging_revenue_table_drop = ("""
DROP TABLE IF EXISTS rev_stage
""")

crm_table_drop = ("""
DROP TABLE IF EXISTS crm
""")

device_table_drop = ("""
DROP TABLE IF EXISTS device
""")

device_type_table_drop = ("""
DROP TABLE IF EXISTS device_type
""")

revenue_table_drop = ("""
DROP TABLE IF EXISTS revenue
""")

# CREATE TABLES

staging_crm_table_create = ("""
CREATE TABLE IF NOT EXISTS crm_stage(
msisdn varchar,
gender varchar,
year_of_birth int,
system_status varchar,
mobile_type varchar,
value_segment varchar
)
""")

staging_device_table_create = ("""
CREATE TABLE IF NOT EXISTS dev_stage(
msisdn varchar,
imei_tac varchar,
brand_name varchar,
model_name varchar,
os_name varchar,
os_vendor varchar
)
""")

staging_revenues_table_create = ("""
CREATE TABLE IF NOT EXISTS rev_stage(
msisdn varchar,
week_number int,
Revenue_usd numeric
)
""")

crm_table_create = ("""
CREATE TABLE IF NOT EXISTS crm(
msisdn varchar,
gender varchar,
year_of_birth int,
system_status varchar,
mobile_type varchar,
value_segment varchar
)
""")

device_table_create = ("""
CREATE TABLE IF NOT EXISTS device(
msisdn varchar,
imei_tac varchar,
device_typeID int
)
""")

device_type_table_create = ("""
CREATE TABLE IF NOT EXISTS device_type(
id int IDENTITY(0,1),
brand_name varchar,
model_name varchar,
os_name varchar,
os_vendor varchar
)
""")

revenue_table_create = ("""
CREATE TABLE IF NOT EXISTS revenue(
msisdn varchar,
week_number int,
Revenue_usd numeric
)
""")

# STAGING TABLES

#staging_crm_copy = (f"""
#    copy crm_stg from {config.get('S3','CRM_DATA')}
#    credentials 'aws_iam_role={config.get('IAM_ROLE', 'ARN')}'
#    CSV
#    compupdate off region 'us-east-1';
#""")

#staging_dev_copy = (f"""
#    copy dev_stg from {config.get('S3','DEV_DATA')}
#    credentials 'aws_iam_role={config.get('IAM_ROLE', 'ARN')}'
#    CSV 
#    compupdate off region 'us-east-1';
#""")

#staging_rev_copy = (f"""
#    copy rev_stg from {config.get('S3','REV_DATA')}
#    credentials 'aws_iam_role={config.get('IAM_ROLE', 'ARN')}'
#    JSON 'auto' 
#    compupdate off region 'us-east-1';
#""")

# FINAL TABLES

# (msisdn, gender, year_of_birth, system_status, mobile_type, value_segment  )
crm_table_insert = ("""
INSERT INTO crm 
(msisdn, gender, year_of_birth, system_status, mobile_type, value_segment  )
(
SELECT msisdn, gender, year_of_birth, system_status, mobile_type, value_segment
FROM crm_stage
)
""")

# (msisdn, imei_tac, device_typeID )
device_table_insert = ("""
INSERT INTO device 
(SELECT *
  FROM dev_stage)
)
""")

# (brand_name ,model_name ,os_name ,os_vendor )
device_type_table_insert = ("""
INSERT INTO device_type 
(SELECT brand_name ,model_name ,os_name ,os_vendor
 FROM dev_stage )
""")

# (msisdn ,week_number ,Revenue_usd )
artist_table_insert = ("""
INSERT INTO revenue 
( SELECT msisdn ,week_number ,Revenue_usd
FROM rev_stage
)
)
""")

# QUERY LISTS

create_table_queries = [staging_crm_table_create, staging_device_table_create, staging_revenues_table_create, crm_table_create, device_table_create, device_type_table_create, revenue_table_create]
drop_table_queries = [staging_crm_table_drop, staging_device_table_drop, staging_revenue_table_drop, crm_table_drop, device_table_drop, device_type_table_drop, revenue_table_drop]

#copy_table_queries = [staging_crm_copy, staging_dev_copy, staging_rev_copy]
#insert_table_queries = [song_table_insert, time_table_insert, artist_table_insert, user_table_insert, songplay_table_insert]

