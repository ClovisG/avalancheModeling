"""
Part of the library doing the opening/parsing of the input files.
Created on 23/02/19
Author : Antoine SANNER
"""
import os
import pickle

import numpy as np

try:
    from PyPDF2 import PdfFileReader
    from camelot import read_pdf

    _pdf_parsing_enabled = True
except ImportError as e:
    print("Import error: " + str(e))
    print("PDF PARSING DISABLED")
    _pdf_parsing_enabled = False

try:
    import xarray as xr
    import netCDF4

    _nc_parsing_enabled = True
except ImportError as e:
    print("Import error: " + str(e))
    print("NC PARSING DISABLED")
    _nc_parsing_enabled = False

from pandas import DataFrame, read_csv, read_html, read_json

from core.utils import *


class DocumentParser:
    # Attribute type hinting
    no_check = ...  # type: bool
    verbose = ...  # type: bool
    _line_scale = ...  # type: int
    _line_tol = ...  # type: int
    _joint_tol = ...  # type: int

    def __init__(self, no_check=False, verbose=False):
        """
        :type no_check: bool
        :param no_check: a boolean specifying if we should check some format properties
        :type verbose: bool
        :param verbose: a boolean specifying if we should print the progress made
        """
        self.no_check = no_check
        self.verbose = verbose
        # These are the parameters for the parsing
        # Mess with them carefully
        self._line_scale = 40
        self._line_tol = 1
        self._joint_tol = 1

    def parse(self, path):
        """
        Parses the file specified in the path and returns a list containing the data found.
        The format of this file can be csv, dataframe, dict, html and json.
        It should be noted that if the no_check option is activated, the number of columns may vary.
        :type path: str
        :param path: the path of the file we should parse
        :rtype dict
        :return a dict containing the data found in pandas.DataFrame objects
        """
        path = os.path.abspath(path)
        if self.verbose:
            print("Parsing: " + path)

        # Is the file there?
        if not os.path.isfile(path):
            raise ParsingException("File: " + path + " not found!")

        # We get the file's extension
        _, file_extension = os.path.splitext(path)

        # We select the right parsing function based on the file's extension
        if file_extension == ".pdf":  # pdf
            tables = self._parse_pdf(path)

        elif file_extension == ".csv":  # csv
            kw = {"encoding": "utf-8", "na_filter": False}
            tables = {path: read_csv(path, **kw)}

        elif file_extension == ".html":  # html
            kw = {"encoding": "utf-8"}
            tables_read = read_html(path, **kw)  # We get a list
            if len(tables_read) > 1:
                raise ParsingException("html files with more than one table are not supported.")
            # If a table has been found
            if tables_read:
                tables = {path: tables_read[0].replace(np.nan, '', regex=True)}  # No "na_filter" option
            else:
                tables = {}

        elif file_extension == ".json":  # json
            kw = {"encoding": "utf-8", "orient": "records"}
            tables = {path: read_json(path, **kw)}

        elif file_extension == ".dataframe":  # Dataframe: raw pickling
            with open(path, 'rb') as f:
                tables = {path: pickle.load(f)}

        elif file_extension == ".dict":  # Pickling as a dict
            tables = self._parse_dict(path)

        elif file_extension == ".nc":  # nc
            if not _nc_parsing_enabled:
                raise ParsingException(".nc file parsing disabled. Please install the required libraries.")

            tables = {path: xr.open_dataset(path).to_dataframe()}

        else:
            raise ParsingException("Unknown file extension: \"" + file_extension + "\"")

        # Reordering of the columns (may be lost during storage)
        for key in tables:
            table = tables[key]

            if is_dataframe_pretty(table):
                tables[key] = table.reindex(PRETTIFIED_TABLE_COLUMN_NAMES[:], axis=1)
            elif is_dataframe_filtered(table):
                tables[key] = table.reindex(FILTERED_TABLE_COLUMN_NAMES[:], axis=1)
            else:
                # Some string information may have been casted to an int
                table.apply(str)
                # Ensuring column names are ints
                table.columns = table.columns.to_series().apply(int)
                # And we need to reorder the columns (Those are int stored as str)
                tables[key] = table.reindex(sorted(table.columns), axis=1)

        # When the first row contains a "Historique" cell, an extra column is added for the description
        # But the first row will be the only one with data in this extra column
        # If the no_check option is not activated, we remove this extra column
        if not self.no_check:
            for key in tables:
                tables[key] = self._drop_extra_column(tables[key], path)

        if self.verbose:
            print("Done!")

        return tables

    def _parse_pdf(self, path):
        """
        Parses the pdf file specified in the path and returns a list containing the data found.
        It should be noted that if the no_check option is activated, the number of columns may vary.
        :type path: str
        :param path: the path of the pdf file we should parse
        :rtype dict
        :return a dict containing the data found in pandas.DataFrame objects
        """
        # Is the pdf file parsing enabled?
        if not _pdf_parsing_enabled:
            raise ParsingException(".pdf file parsing disabled. Please install the required libraries.")

        # We open the pdf file with PyPDF2 to get the number of pages
        with open(path, 'rb') as f:
            page_number = PdfFileReader(f).getNumPages()

        # We want to parse each page of the pdf individually to give some regular feedback on th progress
        # As of 23/02/2019, the parsing of a page can take up to 10 sec with up to around 80 page per document
        tables = {}
        basename, extension = os.path.splitext(path)
        for page_index in range(1, page_number + 1):
            if self.verbose:
                print("Parsing page " + str(page_index) + "...")

            # the camelot.read_pdf call should only return a list containing one element
            # But we can not be too careful
            tables_on_page = read_pdf(path,
                                      pages=str(page_index),
                                      line_scale=self._line_scale,
                                      line_tol=self._line_tol,
                                      joint_tol=self._joint_tol)
            for i, table in enumerate(tables_on_page):
                ending = "_page_{}".format(page_index) + ("_table_{}".format(i) if len(tables_on_page) > 1 else "")
                tables[basename + ending + extension] = table.df

        return tables

    @staticmethod
    def _parse_dict(path):
        """
        Parses the dict file specified in the path and returns a list containing the data found.
        :type path: str
        :param path: the path of the dict file we should parse
        :rtype dict
        :return a dict containing the data found in pandas.DataFrame objects
        """
        # We only allow prettified data as a dict input
        with open(path, 'rb') as f:
            dicts = pickle.load(f)  # We get a list of dicts
        # We check that we have a list of dict
        if not isinstance(dicts, list):
            raise ParsingException("The object stored in the .dict file is not a list")
        for ele in dicts:
            if not isinstance(ele, dict):
                raise ParsingException(
                    "The object stored in the .dict file contains something else than dictionnaries")

        # We check that there is no unknown key
        keyset = {key for d in dicts for key in d.keys()}
        if is_keyset_pretty(keyset):
            column_names = PRETTIFIED_TABLE_COLUMN_NAMES
        elif is_keyset_filtered(keyset):
            column_names = FILTERED_TABLE_COLUMN_NAMES
        else:
            raise ParsingException("Dicts containing unfiltered data are not yet supported.")

        # Rebuilding the DataFrame
        table = DataFrame(columns=column_names[:]).append(dicts, verify_integrity=True, sort=True)
        return {path: table}

    @staticmethod
    def _drop_extra_column(df, path):
        """
        Drops the extra column which may be added when there is an history on the page.
        This functionality is disabled byt the no_check option.
        :type df: DataFrame
        :param df: the DataFrame we need to cleanse
        :rtype DataFrame
        :return the cleansed DataFrame
        """
        # The DataFrame is already pretty
        if is_dataframe_pretty(df):
            return df

        # The table is empty -> nothing to be done
        if df.size <= 0:
            return df
        # We get the first row
        first_row = df.iloc[0].tolist()
        # The first row is not an history -> nothing to be done
        if not re.match("(Historique|History)", first_row[0]):
            return df

        # We look for the index of the extra column and we check that the text has not been split
        cells_text_ind = [i for i, text in enumerate(first_row) if text]
        if len(cells_text_ind) > 2:
            raise ParsingException(
                "There are too many cells containing some text in the history row at " + path)

        extra_col_ind = cells_text_ind[1]
        # We need to check that the extra column has not been dropped previously
        # To do this, we check that there is at least one cell below the history that is not empty
        nb_not_empty_cells = sum([1 for text in df.iloc[:, extra_col_ind].tolist() if text])
        if nb_not_empty_cells != 1:
            # The extra column has already been dropped -> nothing to be done
            return df

        # We move the description to the second column
        df.iloc[0, 1] = df.iloc[0, extra_col_ind]
        # We remove the extra column
        df.drop([df.columns[extra_col_ind]], axis=1, inplace=True)
        # Renaming the columns accordingly
        df.rename(columns={i + 1: i for i in range(extra_col_ind, len(first_row))}, inplace=True)

        return df
