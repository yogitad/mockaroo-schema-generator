CREATE DATABASE IF NOT EXISTS c_nonsp_datasource1;

CREATE EXTERNAL TABLE IF NOT EXISTS c_nonsp_datasource1.dataset1
(
`id` bigint,
`report_id` bigint,
`step_id` bigint,
`create_date` timestamp,
`data_name` string,
`data_value` string
)
PARTITIONED BY
(
`src_date` date
)
STORED AS ORC
LOCATION '/data/c/nonsp/datasource1/dataset1';
