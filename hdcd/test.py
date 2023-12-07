"""
Test functions for hdcd package.
"""
import unittest
import numpy as np
import os
import sys

# directory reach
import plot
import summary

cdi_dummy = pd.read_csv("../dummy_data/cdi_dummy.csv")

class TestCases(unittest.TestCase):


    def test_smoke_test_plot_corr(self):
        """
        simple call function to test whether the program is able to run given
        the correct input
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        location = "United States"
        stratification = "Overall"
        dataframe = cdi_dummy

        plot.plot_corr(sod,
                       health_outcome,
                       location,
                       stratification,
                       dataframe,
                       print_corr=False)

    # one-shot test
    def test_one_shot_test_plot_corr(self):
        """
        feed with ideal input and test the correctness of output
        """

        plot.plot_corr(sod,
                       health_outcome,
                       location,
                       stratification,
                       dataframe,
                       print_corr=False)

        assert np.isclose(knn_regression(n_neighbors,
                           data,
                           query),773.33)

    def test_edge_test_1_plot_corr(self):
        """
        throw TypeError if any of the values are not numerical
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        location = "United States"
        stratification = "Overall"
        dataframe = cdi_dummy.head()

        dataframe["DataValue"] = ["a",
                                  "d",
                                  "a",
                                  "dd",
                                  "sec"]

        with self.assertRaises(TypeError):
            plot.plot_corr(sod,
                           health_outcome,
                           location,
                           stratification,
                           dataframe,
                           print_corr=False)

    def test_edge_test_2_plot_corr(self):
        """
        throw TypeError if all missing
        """

        sod = "Mortality from coronary heart disease"
        health_outcome = "Life expectancy at birth"
        location = "United States"
        stratification = "Overall"
        dataframe = cdi_dummy.head()

        dataframe["DataValue"] = [np.nan,
                                  np.nan,
                                  np.nan,
                                  np.nan,
                                  np.nan,]

        with self.assertRaises(TypeError):
            plot.plot_corr(sod,
                           health_outcome,
                           location,
                           stratification,
                           dataframe,
                           print_corr=False)

    def test_edge_test_3_plot_corr(self):
        """
        throw NameError if any of the variables given are not found
        """

        sod = "No such variable"
        health_outcome = "Life expectancy at birth"
        location = "United States"
        stratification = "Overall"
        dataframe = cdi_dummy.copy()

        with self.assertRaises(NameError):
            plot.plot_corr(sod,
                           health_outcome,
                           location,
                           stratification,
                           dataframe,
                           print_corr=False)
