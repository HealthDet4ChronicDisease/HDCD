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
        data = 

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

        plot.plot_corr()

        query = np.array([5, 4])

        assert np.isclose(knn_regression(n_neighbors,
                           data,
                           query),773.33)
