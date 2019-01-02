CREATE DATABASE IF NOT EXISTS c_nonsp_datasource1;

CREATE EXTERNAL TABLE IF NOT EXISTS c_nonsp_datasource1.dataset2
(
`id` bigint,
`report_id` bigint,
`channel` string,
`user_id` string,
`subscriber` string,
`step_name` string,
`display_name` string,
`node_type` string,
`sub_node_type` string,
`operation_reference` string,
`transition_name` string,
`feedback_flag` int,
`feedback_string` string,
`history` int,
`status` string,
`step_start_time` timestamp,
`step_stop_time` timestamp,
`step_duration` bigint
)
PARTITIONED BY
(
`src_date` date
)
STORED AS ORC
LOCATION '/data/c/nonsp/datasource1/dataset2';
