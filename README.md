# Purpose
Script to read the hive ddl schema file and transform it into Mockaroo style schema that can be used to upload and create the schema automatically.

# Description
Shell script reads all the hql file from the specified hive ddl directory and transforms it to sql format that can be used to parse in python code and from this transformed ddl file creates the Mockaroo compatible schema.

# Steps to Run
sh createMockarooSchema.sh <hive-ddl-directory> <transformed-ddl-directory> <format> <header-flag>

ex: sh createMockarooSchema.sh datasource1-ddl transformed-ddl csv false
