CREATE DATABASE IF NOT EXISTS c_nonsp_datasource1;

CREATE EXTERNAL TABLE IF NOT EXISTS c_nonsp_datasource1.dataset3
(
`id` bigint,
`workflow_name` string,
`channel` string,
`agent_id` string,
`service_id` string,
`fnn` string,
`start_time` timestamp,
`stop_time` timestamp,
`workflow_duration` bigint,
`smpsessionid` string,
`status` string,
`tier1_driver` string,
`tier2_driver` string,
`resolution` string,
`call_type` string,
`modem` string,
`array` string
)
PARTITIONED BY
(
`src_date` date
)
STORED AS ORC
LOCATION '/data/c/nonsp/datasource1/dataset3';
