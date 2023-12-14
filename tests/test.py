"""
Test functions for hdcd package.
"""
import unittest
import os
import sys

import pandas as pd
import numpy as np
import altair as alt
# directory reach

parentdir = os.getcwd()
sys.path.append(parentdir)

import hdcd

cdi_dummy = pd.read_csv("./data/cdi_dummy.csv")

class TestCases(unittest.TestCase):


    def test_smoke_test_plot_corr(self):
        """
        simple call function to test whether the program is able to run given
        the correct input
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        stratification = "Overall"
        dataframe = cdi_dummy

        hdcd.plot_corr(sod,
                       health_outcome,
                       stratification,
                       dataframe,
                       print_corr=False)

    # one-shot test
    def test_one_shot_test_plot_corr(self):
        """
        feed with ideal input and test the correctness of output
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        stratification = "Overall"
        dataframe = cdi_dummy

        hdcd.plot_corr(sod,
                       health_outcome,
                       stratification,
                       dataframe,
                       print_corr=False)

    def test_edge_test_1_plot_corr(self):
        """
        throw TypeError if any of the values are not numerical
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        dataframe["DataValue"] = ["a"] * len(dataframe)

        with self.assertRaises(TypeError):
            hdcd.plot_corr(sod,
                           health_outcome,
                           stratification,
                           dataframe,
                           print_corr=False)

    def test_edge_test_2_plot_corr(self):
        """
        throw TypeError if all missing
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        dataframe["DataValue"] = [np.nan] * len(dataframe)

        with self.assertRaises(TypeError):
            hdcd.plot_corr(sod,
                           health_outcome,
                           stratification,
                           dataframe,
                           print_corr=False)

    def test_edge_test_3_plot_corr(self):
        """
        throw NameError if any of the variables given are not found
        """

        sod = "No such variable"
        health_outcome = "Life expectancy at birth"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        with self.assertRaises(NameError):
            hdcd.plot_corr(sod,
                           health_outcome,
                           stratification,
                           dataframe,
                           print_corr=False)


    def test_smoke_test_geomap(self):
        """
        Smoke test, does it run
        """

        variable = "Life expectancy at birth"
        datatype = "Number"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        hdcd.plot_geomap(variable,
                        datatype,
                        stratification,
                        dataframe)

    def test_one_shot_test_geomap(self):
        """
        Feed with ideal input and test the correctness of output
        """

        variable = "Life expectancy at birth"
        datatype = "Number"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        hdcd.plot_geomap(variable,
                        datatype,
                        stratification,
                        dataframe)

    def test_edge_test_1_geomap(self):
        """
        Feed with ideal input and test the correctness of output
        """

        variable = "NOT EXIST"
        datatype = "Number"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        with self.assertRaises(NameError):
            hdcd.plot_geomap(variable,
                            datatype,
                            stratification,
                            dataframe)

    def test_edge_test_2_geomap(self):
        """
        Feed with ideal input and test the correctness of output
        """

        variable = "Life expectancy at birth"
        datatype = "NOT EXIST"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        with self.assertRaises(NameError):
            hdcd.plot_geomap(variable,
                            datatype,
                            stratification,
                            dataframe)


    def test_edge_test_3_geomap(self):
        """
        Feed with ideal input and test the correctness of output
        """

        variable = "Life expectancy at birth"
        datatype = "NOT EXIST"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        with self.assertRaises(NameError):
            hdcd.plot_geomap(variable,
                            datatype,
                            stratification,
                            dataframe)


    def test_smoke_test_plot_longitudinal_change(self):
        """
        Simple call function to test whether the program is able to run given
        the correct input for plot_longitudinal_change.
        """

        variable = "Life expectancy at birth"
        location = "California"
        stratification = "Overall"
        dataframe = cdi_dummy

        hdcd.plot_longitudinal_change(variable,
                                      location,
                                      stratification,
                                      dataframe)

    def test_one_shot_test_1_plot_longitudinal_change(self):
        """
        Feed with ideal input and test the correctness of the output for
        plot_longitudinal_change.
        """

        variable = "Mortality from coronary heart disease"
        location = "California"
        stratification = "Overall"
        dataframe = cdi_dummy

        chart = hdcd.plot_longitudinal_change(variable,
                                              location,
                                              stratification,
                                              dataframe)

        self.assertIsInstance(chart, alt.FacetChart)

    def test_one_shot_test_2_plot_longitudinal_change(self):
        """
        Feed with different ideal input and test the correctness of the output for
        plot_longitudinal_change.
        """

        variable = "Life expectancy at birth"
        location = "Illinois"
        stratification = "Gender"
        dataframe = cdi_dummy

        chart = hdcd.plot_longitudinal_change(variable,
                                              location,
                                              stratification,
                                              dataframe)

        self.assertIsInstance(chart, alt.FacetChart)

    def test_edge_test_1_plot_longitudinal_change(self):
        """
        Test plot_longitudinal_change with an empty dataframe.
        Expect a ValueError or similar exception when an invalid location is provided.
        """

        variable = "Mortality from coronary heart disease"
        location = "Calfornia"
        stratification = "Overall"
        dataframe = pd.DataFrame()

        with self.assertRaises(KeyError):
            hdcd.plot_longitudinal_change(variable,
                                          location,
                                          stratification,
                                          dataframe)

    def test_edge_test_2_plot_longitudinal_change(self):
        """
        Expect the function to produce an empty plot if any variables are not found.
        """

        variable = "No such variable"
        location = "Washington"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        chart = hdcd.plot_longitudinal_change(variable,
                                              location,
                                              stratification,
                                              dataframe)

        self.assertFalse(hasattr(chart, 'mark_line'))


    ### edge test 1
    def test_edge_test_1_plot_geomap_conditions(self):
        '''
        Provide input with mistakes, see if error is raised
        '''
        dataframe = pd.DataFrame()
        width = 'container'

        with self.assertRaises(ValueError):
            hdcd.plot_geomap_conditions(dataframe,width)

    def test_smoke_test_data_summary(self):
        """
        Smoke test, does it run
        """
        dataframe = cdi_dummy.head()

        hdcd.data_summary(dataframe)

    def test_one_shot_data_summary(self):
        """
        One shot test, getting expected outcome
        """
        dataframe = cdi_dummy.copy()

        hdcd.data_summary(dataframe)

    def test_edge_test_data_summary(self):
        """
        Edge test, no Topic presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"Topic":"NOTOPIC"},inplace=True)
        with self.assertRaises(NameError):
            hdcd.data_summary(dataframe)

    def test_edge_test_2_data_summary(self):
        """
        Edge test, no Question presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"Question":"NOQUESTION"},inplace=True)
        with self.assertRaises(NameError):
            hdcd.data_summary(dataframe)

    def test_edge_test_3_data_summary(self):
        """
        Edge test, no Stratification presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"StratificationCategory1":"NOTOPIC"},
                        inplace=True)
        with self.assertRaises(NameError):
            hdcd.data_summary(dataframe)


    def test_smoke_test_variable_summary(self):
        """
        Smoke test, does it run
        """
        dataframe = cdi_dummy.head()
        variable = "Mortality from coronary heart disease"
        hdcd.variable_summary(variable,
                              dataframe)

    def test_one_shot_variable_summary(self):
        """
        One shot test, getting expected outcome
        """
        dataframe = cdi_dummy.copy()
        variable = "Mortality from coronary heart disease"
        hdcd.variable_summary(variable,
                              dataframe)

    def test_edge_test_variable_summary(self):
        """
        Edge test, no DataValue presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"DataValue":"NODATA"},inplace=True)
        
        variable = "Mortality from coronary heart disease"
        with self.assertRaises(NameError):
            hdcd.variable_summary(variable,
                                  dataframe)

    def test_edge_test_2_variable_summary(self):
        """
        Edge test, no Question presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"Question":"NOQUESTION"},inplace=True)
        variable = "Mortality from coronary heart disease"

        with self.assertRaises(NameError):
            hdcd.variable_summary(variable,
                                  dataframe)

    def test_edge_test_3_variable_summary(self):
        """
        Edge test, no DataValueType presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"DataValueType":"NOTYPE"},
                        inplace=True)
        variable = "Mortality from coronary heart disease"

        with self.assertRaises(NameError):
            hdcd.variable_summary(variable,
                                  dataframe)

    def test_edge_test_4_variable_summary(self):
        """
        Edge test, no YearStart presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"YearStart":"NOYEAR"},
                        inplace=True)

        variable = "Mortality from coronary heart disease"
        with self.assertRaises(NameError):
            hdcd.variable_summary(variable,
                                  dataframe)

    def test_edge_test_5_variable_summary(self):
        """
        Edge test, no LocationAbbr presented in data throw exception
        """
        dataframe = cdi_dummy.copy()
        dataframe.rename(columns = {"LocationAbbr":"NOLOC"},
                        inplace=True)

        variable = "Mortality from coronary heart disease"
        with self.assertRaises(NameError):
            hdcd.variable_summary(variable,
                                  dataframe)




