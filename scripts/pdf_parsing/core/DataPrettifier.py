"""
Part of the library checking the data format and reformating the data into a more usable format.
Created on 23/02/19
Author : Antoine SANNER
"""
import re

from pandas import DataFrame

from core.utils import DataFormatException as DFE, PRETTIFIED_TABLE_COLUMN_NAMES, FILTERED_TABLE_COLUMN_NAMES, \
    is_dataframe_pretty, is_dataframe_filtered


class DataPrettifier:
    @staticmethod
    def keep_events_only(df, event_regex="n°[0-9]+_?[A-Z]?\nid [0-9]+", event_column=0):
        """
        Filters a DataFrame on a column index using a regular expression.
        This is used to only keep rows containing events.
        :type df: DataFrame
        :param df: a DataFrame containing some df
        :type event_regex: str
        :param event_regex: a regular expression which matches with the rows we are interested in
        :type event_column: int
        :param event_column: the column's index where we will test the previous regular expression
        :rtype DataFrame
        :return a DataFrame with where each row is an event (there is no trash)
        """
        # Do we have to do anything?
        if is_dataframe_pretty(df) or is_dataframe_filtered(df) or df.empty:
            return df

        # Filtering
        filtered_df = df[df.iloc[:, event_column].str.contains(event_regex)].copy()
        # Renaming the columns
        filtered_df.rename(columns={i: n for i, n in enumerate(FILTERED_TABLE_COLUMN_NAMES)}, inplace=True)

        return filtered_df

    @staticmethod
    def check_events(df):
        """
        Asserts that the DataFrame passed as argument only contains rows matching a certain format.
        Will also correct some parsing mistakes made by camelot.
        This format is the format used to describe an event (as of 23/02/2019).
        :type df: DataFrame
        :param df: the DataFrame which should be checked. It must only contain events.
        """
        # Do we have to do anything?
        if is_dataframe_pretty(df) or df.empty:
            return df

        # Error the dataframe needs to be filtered
        if not is_dataframe_filtered(df):
            raise Exception("Error: the dataframe needs to be at least filtered.")

        # The following code could be factorised to some extend
        # But for the sake of clarity, it will not

        expected_event_row_length = 42
        for row_index, row in df.iterrows():
            # Converting the Series object into a list
            row = row.tolist()

            # Checking the number of columns
            if len(row) != expected_event_row_length:
                raise DFE("Wrong row length ({}, expected: {}) row {}"
                          .format(len(row), expected_event_row_length, row_index))

            # ATTENTION PLEASE
            # THIS IS WHERE WE MANUALLY CHECK FOR ERRORS STEMMING FROM CAMELOT'S LINE RECOGNITION
            # A FEW OF THIS BUGS HAPPEN WHEN WE HAVE A SITUATION LIKE THIS: "X SO(VERTICALLY) X" CLOSE TOGETHER

            # Bug 1: longueur is shifted to the left
            if re.match(".*[0-9]+$", row[6]) and row[7] == "":
                row[7] = re.findall("[0-9]+$", row[6])[-1]
                row[6] = row[6][:-len(row[7])]

            # Bug 2: direction vent is shifted to the left into vent fort
            if re.match("[NS]?[EO]?\n(?:X|er)", row[17]) and row[18] == "":
                row[17], row[18] = row[17].split("\n")

            # Bug 3: the vent fort and direction vent are switched
            if re.match("[NS]?[EO]?", row[17]) and re.match("(^$|er|\?|X)", row[18]):
                row[17], row[18] = row[18], row[17]

            # Bug 4: the vent fort, direction vent and hauteur neige (on two lines) are merged
            if re.match("[NS]?[EO]?\n[0-9]+-\n(?:er|\?|X)\n[0-9]+", row[16]) and \
                    row[17] == row[18] == "":
                tmp = row[16].split("\n")
                row[16] = tmp[1] + "\n" + tmp[3]
                row[17] = tmp[2]
                row[18] = tmp[0]

            # Bug 5: altitude depart et arrivee merged into date 2
            if re.match("[0-9]{2}/[0-9]{2}/[0-9]{2}\n[0-9]+\n[0-9]+\n[0-9]{2}:[0-9]{2}", row[2]) and \
                    row[3] == row[4] == "":
                tmp = row[2].split('\n')
                row[2] = tmp[0] + '\n' + tmp[-1]
                row[4] = tmp[1]
                row[3] = tmp[2]

            # Weird bug: altitude depart and date2 with date1
            if re.match("[0-9]{2}/[0-9]{2}/[0-9]{2}\n"
                        "[0-9]{2}/[0-9]{2}/[0-9]{2}\n"
                        "[0-9]+\n"
                        "[0-9]{2}:[0-9]{2}\n"
                        "[0-9]{2}:[0-9]{2}", row[1]) and row[2] == row[3] == "":
                tmp = row[1].split('\n')
                row[1] = tmp[0] + "\n" + tmp[3]
                row[2] = tmp[1] + "\n" + tmp[4]
                row[3] = tmp[2]

            # Last Bug: due to the text being sometimes on multiple lines, it can be merged
            for index in [1, 2, 16]:
                if re.match("(?:.*\n){2,}.*", row[index]) and row[index + 1] == "":
                    tmp = row[index].split('\n')
                    row[index] = '\n'.join(tmp[i] for i in range(0, len(tmp), 2))
                    row[index + 1] = '\n'.join(tmp[i] for i in range(1, len(tmp), 2))

            # ACTUAL CHECK START
            error_msg_end = " in row " + str(row_index)

            # Event id
            DFE.assert_format("n°[0-9]+_?[A-Z]?\nid [0-9]+", row[0], "Wrong \"number id\"" + error_msg_end)

            # Dates
            # There is at least one entry with no dates WTF?
            DFE.assert_format("(^$|[0-9]{2}/[0-9]{2}/[0-9]{2}\n[0-9]{2}:[0-9]{2})", row[1],
                              "Wrong \"date1\"")  # date1: jj/mm/yy\nhh:mm
            DFE.assert_format("(^$|[0-9]{2}/[0-9]{2}/[0-9]{2}\n[0-9]{2}:[0-9]{2})", row[2],
                              "Wrong \"date2\"")  # date2: jj/mm/yy\nhh:mm

            # Altitudes
            # Either an optional altitude or multiple optional altitudes for different branches
            DFE.assert_format("(^$|\?|er|[0-9]+|(?:[A-Z] (?:\?|[0-9]+)?)+)", row[3],
                              "Wrong \"release altitude\"")  # altitude départ
            # Either an optional altitude or multiple optional altitudes for different branches
            DFE.assert_format("(^$|\?|er|[0-9]+|(?:[A-Z] (?:\?|[0-9]+)?)+)", row[4],
                              "Wrong \"runout altitude\"")  # altitude arrivée
            DFE.assert_format("(^$|X)", row[5], "Wrong \"opposite slope\"")  # versant opposé
            DFE.assert_format("(^$|X)", row[6], "Wrong \"flat area\"")  # zone plane

            # Depots
            DFE.assert_format("(^$|[0-9]+|[0-9]+\.[0-9]+)", row[7], "Wrong \"length\"")  # longueur
            DFE.assert_format("(^$|[0-9]+|[0-9]+\.[0-9]+)", row[8], "Wrong \"width\"")  # largeur
            DFE.assert_format("(^$|[0-9]+|[0-9]+\.[0-9]+)", row[9], "Wrong \"height\"")  # hauteur

            # Caracteristiques
            DFE.assert_format("(^$|[0-9])", row[10], "Wrong \"A - type of departure\"")  # A - type depart
            DFE.assert_format("(^$|[0-9])", row[11], "Wrong \"B - ground visibility\"")  # B - sol visible
            DFE.assert_format("(^$|[0-9])", row[12], "Wrong \"C - wet / dry snow\"")  # C - humidité depart
            DFE.assert_format("(^$|[0-9])", row[13], "Wrong \"D - path - slope\"")  # D - couloir - versant
            DFE.assert_format("(^$|[0-9])", row[14], "Wrong \"E - aerosol ?\"")  # E - aérosol ?
            DFE.assert_format("(^$|[0-9])", row[15], "Wrong \"F - snow deposit\"")  # F - neige dépôt

            # Meteo 3 jours precedents
            DFE.assert_format("(^$|[0-9]+-\n?[0-9]+|0|>100|\?|er)", row[16],  # ATTENTION THIS IS USED IN BUG COR 4
                              "Wrong \"snow depth\"")  # hauteur de neige
            DFE.assert_format("(^$|\?|X|er)", row[17], "Wrong \"strong wind\"")  # vent fort
            DFE.assert_format("([NS]?[EO]?|er)", row[18],
                              "Wrong \"wind direction\"")  # direction vent (cardinal direction)
            DFE.assert_format("(^$|\?|X|er)", row[19], "Wrong \"mild weather\"")  # redoux
            DFE.assert_format("(^$|\?|X|er)", row[20], "Wrong \"rain\"")  # pluie

            # Meteo 4h precedentes
            DFE.assert_format("(^$|\?|X|er)", row[21], "Wrong \"snow\"")  # neige
            DFE.assert_format("(^$|\?|X|er)", row[22], "Wrong \"rain\"")  # pluie
            DFE.assert_format("(^$|\?|X|er)", row[23], "Wrong \"strong wind\"")  # vent fort
            DFE.assert_format("(^$|\?|X|er)", row[24], "Wrong \"clear sky\"")  # ciel clair
            DFE.assert_format("(^$|\?|X|er)", row[25], "Wrong \"clouds\"")  # nuages
            DFE.assert_format("(^$|\?|X|er)", row[26], "Wrong \"fog\"")  # brouillard

            # Causes
            DFE.assert_format("(^$|\?|X|er)", row[27], "Wrong \"natural\"")  # naturelle
            DFE.assert_format("(^$|\?|X|er)", row[28], "Wrong \"accidental\"")  # involontaire
            DFE.assert_format("(^$|\?|X|er)", row[29], "Wrong \"artificial\"")  # artificielle
            DFE.assert_format("(^$|\?|X|er)", row[30], "Wrong \"unknown\"")  # inconnue

            # Victimes
            DFE.assert_format("(^$|\?|X|er)", row[31], "Wrong \"no victim\"")  # néant
            DFE.assert_format("(^$|[0-9]+|X)", row[32], "Wrong \"injured\"")  # blessés
            DFE.assert_format("(^$|[0-9]+|X)", row[33], "Wrong \"dead\"")  # morts

            # Degats ou lieux atteints
            DFE.assert_format("(^$|X|er)", row[34], "Wrong \"no damage\"")  # néant
            DFE.assert_format("(^$|X|er)", row[35], "Wrong \"construction\"")  # construction
            DFE.assert_format("(^$|X|er)", row[36], "Wrong \"posts, poles\"")  # poteaux
            DFE.assert_format("(^$|X|er)", row[37], "Wrong \"forest\"")  # forêt
            DFE.assert_format("(^$|X|er)", row[38], "Wrong \"roads\"")  # routes
            DFE.assert_format("(^$|X|er)", row[39], "Wrong \"rivers\"")  # cours d'eau

            # Obs
            DFE.assert_format("(^$|I|B|BS|G|D|GD|er)", row[40],  # French and English
                              "Wrong \"visibility\"")  # visibilité (I = Incomplète, B = Bonne, BS = Bonne sauf départ)
            DFE.assert_format("(^$|O|N|Y|N|er)", row[41], "Wrong \"alerte event DB\"")  # alerte bd event (OUI/NON)

    @staticmethod
    def prettify(df):
        """
        Rearranges the data et replaces the different values with more usable ones.
        For example: "X" will become True, "", "er", "?" will become False.
        :type df: DataFrame
        :param df: the DataFrame which should be prettified
        :rtype DataFrame
        :return a pretty Dataframe
        """

        def checkable_conv(text):
            return {"": False,
                    "?": "",
                    "er": "",
                    "X": True,
                    "O": True,  # French and English version of the last column
                    "N": False,
                    "Y": True}[text]

        def optional_int_conv(text):
            try:
                return int(text)
            except ValueError:
                return ""

        # Do we have to do anything?
        if is_dataframe_pretty(df) or df.empty:
            return df

        # Error the dataframe needs to be filtered
        if not is_dataframe_filtered(df):
            raise Exception("Error: the dataframe needs to be at least filtered.")

        # The column's names are their Label -> the DataFrame only contains events
        pretty_df = DataFrame(columns=PRETTIFIED_TABLE_COLUMN_NAMES)

        index = 1
        for row_index, row in df.iterrows():
            row = row.tolist()
            pretty_row = []

            # Prettifying
            # Event id (there's a split to be done)
            num, id_text = row[0].split("\n")
            pretty_row.append(num[2:])
            pretty_row.append(id_text[3:])

            # Dates (replace "\n" with " ")
            pretty_row.append(row[1].replace("\n", " "))
            pretty_row.append(row[2].replace("\n", " "))

            # Altitudes
            if re.match("(?:[A-Z] (?:\?|[0-9]+)?)+", row[3]):  # altitude départ
                # We have multiple branches
                pretty_row.append(max(re.findall("[0-9]+", row[3])))
            else:
                # We have an optional int
                pretty_row.append(optional_int_conv(row[3]))
            if re.match("(?:[A-Z] (?:\?|[0-9]+)?)+", row[4]):  # altitude arrivée
                # We have multiple branches
                pretty_row.append(min(re.findall("[0-9]+", row[3])))
            else:
                # We have an optional int
                pretty_row.append(optional_int_conv(row[4]))
            pretty_row.append(checkable_conv(row[5]))  # versant opposé
            pretty_row.append(checkable_conv(row[6]))  # zone plane

            # Depots
            # We can either have nothing, an int or a float
            for index in range(7, 10):
                # Do we have a float?
                if re.match("[0-9]+\.[0-9]+", row[index]):
                    pretty_row.append(float(row[index]))
                # Or else we have an optional int
                else:
                    pretty_row.append(optional_int_conv(row[index]))

            # Caracteristiques
            for index in range(10, 16):
                pretty_row.append(optional_int_conv(row[index]))

            # Meteo 3 jours precedents
            # We can either have nothing, 0 or a range  # hauteur de neige
            # Do we have a range?
            if re.match("[0-9]+-\n?[0-9]+", row[16]):
                start, end = row[16].split('-')
                pretty_row.append(int(start))
                pretty_row.append(int(end))
            # Do we have '>100'?
            if row[16] == '>100':
                pretty_row.append(100)
                pretty_row.append("")
            # Or else we have an optional int
            else:
                pretty_row.append(optional_int_conv(row[16]))
                pretty_row.append("")

            pretty_row.append(checkable_conv(row[17]))  # vent fort
            # We have to split the data for each cardinal direction
            for direction in "NESO":
                pretty_row.append(direction in row[18])  # direction vent (cardinal direction)
            pretty_row.append(checkable_conv(row[19]))  # redoux
            pretty_row.append(checkable_conv(row[20]))  # pluie

            # Meteo 4h precedentes + Causes (checkable conv)
            for index in range(21, 31):
                pretty_row.append(checkable_conv(row[index]))

            # Victimes
            pretty_row.append(checkable_conv(row[31]))  # néant
            pretty_row.append(optional_int_conv(row[32]))  # blessés
            pretty_row.append(optional_int_conv(row[33]))  # morts

            # Degats ou lieux atteints
            for index in range(34, 40):
                pretty_row.append(checkable_conv(row[index]))

            # Obs
            # This field probably will not be used, but we will include it anyway
            # But it will not be prettified
            pretty_row.append(
                optional_int_conv(row[40]))  # visibilité (I = Incomplète, B = Bonne, BS = Bonne sauf départ)
            pretty_row.append(optional_int_conv(row[41]))  # alerte bd event (OUI/NON)

            pretty_df.loc[index] = pretty_row
            index += 1

        return pretty_df
