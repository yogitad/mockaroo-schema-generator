#!/bin/sh

datasource_ddl_dir=$1
transformed_ddl_dir=$2
format=$3
header=$4
# First Transform the ddls to Mockaroo create schema style
pwd_dir=$(pwd)
# Created transformed ddl directory
for hqlfileDir in `find . -name *.hql -type f -exec sh -c 'echo $(dirname $0)' {} \;` ; do mkdir -p $transformed_ddl_dir/$hqlfileDir; done
# Changing string datatype to text as sqlparse library used to parse create table statement expects text datatype for parsing
for ff in `find $datasource_ddl_dir -name *.hql`; do cat $ff | sed -e '/CREATE DATABASE*/d'  | sed 's/CREATE EXTERNAL/CREATE/' | sed '1,/PARTITIONED BY/!d' |  sed '/PARTITIONED BY/d' | sed 's/`//g' | sed 's/string/text/g' |  sed 's/timestamp/date/g'  > $transformed_ddl_dir/$ff.mod ;  done

# Invoke the createSchema script
if [ $header == "true" ]
then
    headerOpt="--header"
else
    headerOpt=""
fi
for ddlfile in `find $transformed_ddl_dir -name *.hql.mod`
do
    echo $ddlfile
    python createSchemaFromDDL.py -f $ddlfile -t $format -o $pwd_dir/output-schema $headerOpt
done

