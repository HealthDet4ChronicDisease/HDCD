"""
Test functions for hdcd package.
"""
import unittest
import os
import sys

import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd
# directory reach

parentdir = os.getcwd()
sys.path.append(parentdir)
sys.path.append('../hdcd')

import hdcd
from hdcd.data_wrangling import AoU_socioeconomic
from hdcd.data_wrangling import AoU_conditions

cdi_dummy = pd.read_csv("./data/cdi_dummy.csv")
conditions_csv = pd.read_csv("./data/conditions.csv")


# recommended geoshapes file and ZIP codes for US counties file
geo_df = 'https://gist.githubusercontent.com/sdwfrost/\
d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/\
counties.geojson'
county_df = 'https://raw.githubusercontent.com/scpike/us-state-county-zip/\
master/geo-data.csv'
observations_df = pd.read_csv("./data/observation_data.csv")
conditions_df = pd.read_csv("./data/condition_data.csv")

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


    ### smoke test
    def test_smoke_test_plot_geomap_conditions(self):
        '''
        conducts a smoke test
        with the right inputs, program should run fine
        '''
        dataframe = conditions_csv.copy()
        width = 'container'

        hdcd.plot_geomap_conditions(dataframe,width)

    ### one-shot test 1
    def test_one_shot_test_1_plot_geomap_conditions(self):
        '''
        Provide good input and test to see if output looks good
        '''
        dataframe = conditions_csv.copy()
        width = 'container'

        hdcd.plot_geomap_conditions(dataframe,width)

    ### edge test 1
    def test_edge_test_1_plot_geomap_conditions(self):
        '''
        Provide input with mistakes, see if error is raised
        '''
        dataframe = conditions_csv.copy()
        width='container'

        dataframe.rename(columns = {"county":"NO_county"},
                        inplace=True)
        with self.assertRaises(NameError):
            hdcd.plot_geomap_conditions(dataframe,
                                        width)

        #with self.assertRaises(NameError):
         #  hdcd.plot_geomap_conditions(dataframe,
          #                          width)
    ### edge test 2
    def test_edge_test_2_plot_geomap_conditions(self):
        '''
        Provide input with mistakes, see if error is raised
        '''
        dataframe = pd.DataFrame()
        width='container'

        with self.assertRaises(ValueError):
            hdcd.plot_geomap_conditions(dataframe,
                                    width)


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


    def test_smoke_test_load_geoshapes(self):
        """
        Smoke test, does it run
        """
        aou = AoU_socioeconomic(df=pd.DataFrame(), geo_df=geo_df, county_df=county_df)

        aou.load_geoshapes()

    def test_one_shot_load_geoshapes(self):
       """
       One-shot test, getting expected outcome
       """
       aou = AoU_socioeconomic(df=pd.DataFrame(),
                               geo_df=geo_df,
                               county_df=county_df)

       result = aou.load_geoshapes()

       self.assertIsInstance(result, gpd.GeoDataFrame)
       self.assertIn('state_fips', result.columns)
       self.assertEqual(result['state_fips'].dtype, 'int64')

       original_counties = gpd.read_file(geo_df)
       self.assertEqual(len(result), len(original_counties))

    def test_edge_test_load_geoshapes(self):
        """
        Edge test for load_geoshapes with non-string geo_df
        """
        aou = AoU_socioeconomic(df=pd.DataFrame(),
                                geo_df=123,
                                county_df=county_df)
        with self.assertRaises(ValueError):
            aou.load_geoshapes()

    def test_edge_test_2_load_geoshapes(self):
        """
        Edge test for load_geoshapes with empty string geo_df
        """
        aou = AoU_socioeconomic(df=pd.DataFrame(),
                                geo_df='',
                                county_df=county_df)
        with self.assertRaises(ValueError):
            aou.load_geoshapes()

    def test_edge_test_3_load_geoshapes(self):
        """
        Edge test for load_geoshapes with empty string geo_df
        """
        aou = AoU_socioeconomic(df=pd.DataFrame(),
                                geo_df='https://invalid-url.com',
                                county_df=county_df)
        with self.assertRaises(ValueError):
            aou.load_geoshapes()

    def test_smoke_test_load_counties_zip(self):
        """
        Smoke test, does it run
        """
        aou = AoU_socioeconomic(
            df=pd.DataFrame(),
            geo_df=geo_df,
            county_df=county_df)

        aou.load_counties_zip()

    def test_one_shot_test_load_counties_zip(self):
        """
        One-shot test, getting expected outcome
        """
        aou = AoU_socioeconomic(
            df=pd.DataFrame(),
            geo_df=geo_df,
            county_df=county_df)

        result = aou.load_counties_zip()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('NAME', result.columns)

    def test_edge_test_1_load_counties_zip(self):
        """
        Edge test for load_counties_zip with invalid URL
        """
        aou = AoU_socioeconomic(
            df=pd.DataFrame(),
            geo_df=geo_df,
            county_df='https://invalid-url.com')

        with self.assertRaises(ValueError):
            aou.load_counties_zip()

    def test_smoke_test_merge_geoshapes_counties_zip(self):
        """
        Smoke test, does it run
        """
        # Instance of AoU_socioeconomic class
        aou = AoU_socioeconomic(
            df=pd.DataFrame(),
            geo_df=geo_df,
            county_df=county_df)

        aou.merge_geoshapes_counties_zip()

    def test_one_shot_merge_geoshapes_counties_zip(self):
        """
        One shot test, getting expected outcome
        """
        aou = AoU_socioeconomic(
            df=pd.DataFrame(),
            geo_df=geo_df,
            county_df=county_df)

        result = aou.merge_geoshapes_counties_zip()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(set(['state_fips', 'STATEFP', 'zipcode', 'NAME', 'state']).issubset(set(result.columns)))

    def test_smoke_test_zip_socioeconomic(self):
        """
        Smoke test, does it run
        """
        # Sample socioeconomic dataframe with required columns
        data = {
            'person_id': [1, 2, 3],
            'observation_datetime': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'ZIP_code': [12345, 67890, 54321],
            'some_other_column': ['value1', 'value2', 'value3']
        }
        sample_df = pd.DataFrame(data)

        aou = AoU_socioeconomic(
            df=sample_df,
            geo_df=geo_df,
            county_df=county_df)

        aou.zip_socioeconomic()

    def test_one_shot_test_zip_socioeconomic(self):
        """
        One-shot test, getting expected outcome
        """
        # Sample socioeconomic dataframe with required columns
        data = {
            'person_id': [1, 2, 3],
            'observation_datetime': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'ZIP_code': [12345, 67890, 54321],
            'some_other_column': ['value1', 'value2', 'value3']
        }
        sample_df = pd.DataFrame(data)

        aou = AoU_socioeconomic(
            df=sample_df,
            geo_df=geo_df,
            county_df=county_df)

        result = aou.zip_socioeconomic()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(set(['ZIP_code', 'some_other_column']).issubset(set(result.columns)))
        self.assertEqual(len(result), 3)

    def test_edge_test_1_zip_socioeconomic(self):
        """
        Edge test: Empty Pandas DataFrame input for zip_socioeconomic
        """

        aou = AoU_socioeconomic(df=pd.DataFrame,
                                geo_df= geo_df,
                                county_df=county_df)

        with self.assertRaises(ValueError):
            result = aou.zip_socioeconomic()

    def test_edge_test_2_zip_socioeconomic(self):
        """
        Edge test for missing columns (person_id or observation_datetime)
        in Pandas DataFrame input for zip_socioeconomic
        """
        # Create a sample DataFrame without person_id or observation_datetime columns
        data = {
            'ZIP_code': [12345, 67890],
            'column_without_id': ['value1', 'value2']
        }
        missing_columns_df = pd.DataFrame(data)

        aou = AoU_socioeconomic(
            df=missing_columns_df,
            geo_df=geo_df,
            county_df=county_df)

        with self.assertRaises(KeyError):
            result = aou.zip_socioeconomic()

    # For load_counties_zip
    ### smoke test
    def test_smoke_test_load_counties_zip(self):
        '''
        conducts a smoke test
        with the right inputs, program should run fine
        '''
        aou_lcz = AoU_conditions(pd.DataFrame(),
                                    geo_df = geo_df,
                                    county_df = county_df,
                                    observations_df = observations_df)


        #data_wrangling.load_counties_zip(self.county_df)
        try:
            aou_lcz.load_counties_zip()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")




    ### one-shot test 1
    def test_one_shot_test_1_load_counties_zip(self):
        '''
        Provide good input and test to see if output looks good
        '''
        aou_lcz = AoU_conditions(pd.DataFrame(),
                                    geo_df = geo_df,
                                    county_df = county_df,
                                    observations_df = observations_df)


        #data_wrangling.load_counties_zip(self.county_df)
        try:
            aou_lcz.load_counties_zip()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")




    ### edge test 1
    def test_edge_test_1_load_counties_zip(self):
        '''
        Provide input with mistakes, see if error is raised
        '''
        aou_lcz = AoU_conditions(pd.DataFrame(),
                                    geo_df = geo_df,
                                    county_df = 1234567,
                                    observations_df = observations_df)
        with self.assertRaises(ValueError):
            aou_lcz.load_counties_zip()


    ### edge test 2
    def test_edge_test_2_load_counties_zip(self):
        '''
        Provide input with mistakes, see if error is raised
        '''
        aou_lcz = AoU_conditions(pd.DataFrame(),
                                    geo_df = 123321,
                                    county_df = county_df,
                                    observations_df = observations_df)
        with self.assertRaises(ValueError):
            aou_lcz.load_counties_zip()





    ### For threshold_conditions
    ### smoke test
    def test_smoke_test_threshold_conditions(self):
        '''
        conducts a smoke test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df)
        try:
            aou_tc.threshold_conditions()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")


    ### one-shot test 1
    def test_one_shot_test_1_threshold_conditions(self):
        '''
        Provide good input and test to see if output looks good
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df)
        try:
            aou_tc.threshold_conditions()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")


    ### For observation zip
    ### smoke test ###
    def test_smoke_test_observation_zip(self):
        '''
        conducts a smoke test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df
                                )
        try:
            aou_tc.observation_zip()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")

    ### one shot test 1 ###
    def test_one_shot_test_1_observation_zip(self):
        '''
        conducts a one shot test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df
                                )
        try:
            aou_tc.observation_zip()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")





    ### For merge conditions observation
    ### smoke test ###
    def test_smoke_test_merge_conditions_observation(self):
        '''
        conducts a smoke test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df
                                )
        try:
            aou_tc.merge_conditions_observation()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")

    ### one shot test 1 ###
    def test_one_shot_test_1_merge_conditions_observation(self):
        '''
        conducts a one shot test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df
                                )
        try:
            aou_tc.merge_conditions_observation()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")



    ### For counties_groupby_count
    ### smoke test ###
    def test_smoke_test_counties_groupby_count(self):
        '''
        conducts a smoke test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df
                                )
        try:
            aou_tc.counties_groupby_count()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")

    ### one shot test 1 ###
    def test_one_shot_test_1_counties_groupby_count(self):
        '''
        conducts a one shot test
        with the right inputs, program should run fine
        '''
        aou_tc = AoU_conditions(conditions_df = conditions_df,
                                observations_df = observations_df,
                                county_df = county_df,
                                geo_df = geo_df
                                )
        try:
            aou_tc.counties_groupby_count()
        except Exception as e:
            self.fail(f"load_counties_zip raised an exception: {e}")
