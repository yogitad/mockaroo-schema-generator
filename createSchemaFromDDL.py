#!/bin/py

import sys
import argparse
import ConfigParser
from ConfigParser import NoSectionError, NoOptionError, DuplicateSectionError, Error
from jinja2 import Environment, FileSystemLoader
import sqlparse, re
from sqlparse import *

def parse_command_line():
    """
    Command line parser.
    """

    parser = argparse.ArgumentParser(description='Argument parser for reading ddl schema and create Mockaroo schema json')
    parser.add_argument('-f', '--ddl-schema-file',
        dest='ddlSchemaFile',
        help='Input schema ddl file based off which mockaroo schema will be generated',
        required=True)
    parser.add_argument('-o', '--output-dir',
        dest='outputDir',
        help='Output directory',
        required=True)
    parser.add_argument('-t', '--file-format',
        dest='fileFormat',
        help='File format',
        required=True)
    parser.add_argument('--header',
        dest='headerFlag',
        required=False,
        action='store_true',
        help='If output data requires header')

    try:
        results = parser.parse_args()
    except IOError, msg:
        results=None
        parser.error(str(msg))

    return results

def extract_definitions(token_list):
    # assumes that token_list is a parenthesis
    definitions = []
    tmp = []
    # grab the first token, ignoring whitespace. idx=1 to skip open (
    tidx, token = token_list.token_next(1)
    while token and not token.match(sqlparse.tokens.Punctuation, ')'):
        tmp.append(token)
        # grab the next token, this times including whitespace
        tidx, token = token_list.token_next(tidx, skip_ws=False)
        # split on ",", except when on end of statement
        if token and token.match(sqlparse.tokens.Punctuation, ','):
            definitions.append(tmp)
            tmp = []
            tidx, token = token_list.token_next(tidx)
    if tmp and isinstance(tmp[0], sqlparse.sql.Identifier):
        definitions.append(tmp)
    return definitions


if __name__ == "__main__":
    # Parse command line
    parsed_args = parse_command_line()

    # Pass the directory containing the template:
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    # Map of field types and templates
    field_type_template_map = {
            'bigint':'dataTypeNumber.json',
            'text':'dataTypeString.json',
            'date':'dataTypeDate.json',
            }
    # Read the fields from ddl file
    sourceDddlFile = open(parsed_args.ddlSchemaFile, 'r')
    sqlStatememt = sourceDddlFile.read()
    ddls = sqlparse.parse(sqlStatememt)
    schemaName=str(ddls[0].tokens[11])

    # extract the parenthesis which holds column definitions
    parsed = sqlparse.parse(sqlStatememt)[0]

    # Helper function, that splits the column definitions

    _, par = parsed.token_next_by(i=sqlparse.sql.Parenthesis)
    columns = extract_definitions(par)

    columnsSchema = ""
    idx=0
    for column in columns:
        if idx != 0:
            columnsSchema += ",\n"
        fieldName = column[0]
        fieldType = ''.join(str(t) for t in column[1:])
        print fieldType
        #print('NAME: {name:10} DEFINITION: {definition}'.format(
        #    name=column[0], definition=''.join(str(t) for t in column[1:])))
        template = env.get_template(field_type_template_map[fieldType.strip()])
        output = template.render(field_name=fieldName)
        columnsSchema += output
        idx = idx + 1

    finalTemplate = env.get_template('masterSchema.json')
    if parsed_args.headerFlag == True:
        parsed_args.headerFlag = "true"
    else:
        parsed_args.headerFlag = "false"

    outputFinal = finalTemplate.render(file_format=parsed_args.fileFormat, columns_schema=columnsSchema, header_flag=parsed_args.headerFlag, database_table_name=schemaName)
    print(outputFinal)


# Read the ddl schema

