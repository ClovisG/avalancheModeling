#!/usr/bin/python3
"""
Command line interface.
Created on 23/02/19
Author : Antoine SANNER
"""
import argparse
import traceback

from core import *

# Parser setup
parser = argparse.ArgumentParser(prog="EPA Document Parser",
                                 description="Command line interface for the EPA Document parsing library. "
                                             "It will also only return the rows corresponding to an vent and it will"
                                             " check the format of the data (see the -n and -p options).")
# Input files
parser.add_argument('-i', '--input', action='store', nargs='+', type=str, required=True,
                    help="A list of files to parse.", dest="input_files")
# Output format
parser.add_argument('-f', '--format', action='store', type=str, default="csv",
                    choices=["csv", "dataframe", "dict", "html", "json"],
                    help="The file format of the output. "
                         "The name of the output files will be the same as the name of the input file "
                         "(minus its extension).",
                    dest="file_format")
# Verbosity
parser.add_argument('-v', '--verbose', action='store_true', help="Makes the parsing more verbose.", dest="verbose")
# Ignore exceptions
parser.add_argument('-e', '--ignore-exceptions', action='store_true',
                    help="Ignores a file if an exception is raised rather than exiting the whole program.",
                    dest="ignore_exceptions")

# Mutually exclusive options
exclusive_group = parser.add_mutually_exclusive_group()
# Output dir
exclusive_group.add_argument('-o', '--output-dir', action='store', type=str, default="",
                             help="The destination folder. By default the file generated will be "
                                  "in the same folder as the corresponding input file.",
                             dest="output_dir")
# Merge tables
exclusive_group.add_argument('-m', '--merge', action='store', type=str, default="",
                             help="Merges all the tables which where extracted into a single one "
                                  "(you need to specify a destination). "
                                  "If only one table is merged, it will simply be saved at the specified destination.",
                             dest="merge_dest")
# Check only
exclusive_group.add_argument('-c', '--check-only', action='store_true',
                             help="Will only check the data format of the events and will not save the result.",
                             dest="check_only")

# Mutually exclusive options
exclusive_group = parser.add_mutually_exclusive_group()
# No check
exclusive_group.add_argument('-n', '--no-check', action='store_true',
                             help="Disables the data format check and allows you to get the raw table. "
                                  "Some mistakes done during the parsing of a pdf file will not fixed.",
                             dest="no_check")
# Prettify
exclusive_group.add_argument('-p', '--prettify', action='store_true',
                             help="Enables the prettifying of the data. "
                                  "This will for instance convert \"X\", \"er\", \"\" and so on into True, False... "
                                  "This has no effect on pretty data.",
                             dest="prettify")

args = parser.parse_args()

tables = {}
prettifier = DataPrettifier()
doc_parser = DocumentParser(verbose=args.verbose, no_check=args.no_check)

# Handling the data
for path in args.input_files:
    path = os.path.abspath(path)
    try:
        # Parsing
        tables_in_file = doc_parser.parse(path)

        # Keeping events only - Checking their format - Prettifying
        if not args.no_check:
            for path in tables_in_file:
                if not is_dataframe_pretty(tables_in_file[path]):
                    # Keeping events only
                    new_table = prettifier.keep_events_only(tables_in_file[path])

                    # Checking
                    prettifier.check_events(new_table)

                    # Prettifying
                    if args.prettify:
                        new_table = prettifier.prettify(new_table)

                    tables_in_file[path] = new_table

        # Should we keep them?
        if not args.check_only:
            tables.update(tables_in_file)

    except Exception as e:
        print("Parsing error in file: " + path)
        traceback.print_tb(e.__traceback__)
        print(e)
        if not args.ignore_exceptions:
            exit(1)

# Merging and saving to dest
exporter = DataFrameExporter()
if args.merge_dest:
    table_iter = iter(tables.values())

    new_table = None
    # If there is at least one table not empty to save
    for table in table_iter:
        if not table.empty:
            new_table = table
            break

    new_tables_prettiness = get_dataframe_prettiness(new_table)
    if table_iter is not None:
        for table in table_iter:
            # Prettiness check
            if not get_dataframe_prettiness(table) != new_tables_prettiness:
                print("Error: one of the tables to be merged is less pretty than the others:")
                exit(1)

            if not table.empty:
                new_table = new_table.append(table, ignore_index=True)
        exporter.export(args.merge_dest, new_table, f=args.file_format)

# Default Saving
else:
    for path in tables:
        base_dir, base_name = os.path.split(path)

        # Output directory option
        if args.output_dir:
            base_dir = os.path.abspath(args.output_dir)

        # Removing the extension
        base_name, _ = os.path.splitext(base_name)

        new_path = base_dir + os.sep + base_name + "." + args.file_format
        exporter.export(new_path, tables[path], f=args.file_format)
