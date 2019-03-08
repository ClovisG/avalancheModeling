"""
Part of the library  storing the tables extracted from the input files.
Created on 23/02/19
Author : Antoine SANNER
"""
from pandas import DataFrame
import pickle


class DataFrameExporter:
    @staticmethod
    def export(path, df, f="csv"):
        """
        :type path: str
        :param path: The path where the output should be stored.
        :type df: DataFrame
        :param df: The DataFrame which should be stored.
        :type f: str
        :param f: File format. Can be csv, dataframe, dict, html and json.
        """
        if f == "csv":
            # To csv
            kw = {
                'encoding': 'utf-8',
                'index': False,
                'header': True,
                'quoting': 1
            }
            df.to_csv(path, **kw)

        elif f == "dataframe":
            # To dataframe
            with open(path, "wb") as stream:
                pickle.dump(df, stream, protocol=pickle.HIGHEST_PROTOCOL)

        elif f == "dict":
            # To dict -> there is a conversion to do
            events = []
            for row_index, row in df.iterrows():
                event = {}
                for name, value in row.iteritems():
                    event[name] = value
                events.append(event)
            with open(path, "wb") as stream:
                pickle.dump(events, stream, protocol=pickle.HIGHEST_PROTOCOL)

        elif f == "html":
            # To html
            html_string = df.to_html()
            with open(path, 'w') as stream:
                stream.write(html_string)

        elif f == "json":
            # To json
            kw = {'orient': 'records'}
            json_string = df.to_json(**kw)
            with open(path, 'w') as f:
                f.write(json_string)

        else:
            # Unknown type
            raise Exception("Unknown output format: " + f)
