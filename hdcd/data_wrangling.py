"""
This Python script defines a class for data wrangling the
All of US socioeconomic dataset.

This script requires `numpy`, `pandas`, and `geopandas` within
the Python environment you are running this in.

The class accepts Pandas DataFrames, csv files, and zip files of geoJSON.
The class consists of functions:
    * load_geoshapes
    * load_counties_zip
    * merge_geoshapes_counties_zip
    * zip_socioeconomic
    * merge_county_socioeconomic

This script can be imported as a module.
"""
import os

import numpy as np
import pandas as pd
import geopandas as  gpd

# recommended geoshapes file and ZIP codes for US counties file
geo_df = 'https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson'
zip_df = 'https://raw.githubusercontent.com/scpike/us-state-county-zip/master/geo-data.csv'

class AoU_socioeconomic():
    """
    This class consists of multiple functions to wrangle and clean
    the All of US dataset to produce interactive visualizations
    specifically for county level socioeconomic data, as defined by 
    All of Us.
    """
    def __init__(self, df, geo_df, zip_df):
        """
        This function initializes objects to be passed in the class.

        Args:
            df (DataFrame): All of US ZIP code and socioeconomic
                DataFrame to be passed from SQL query
            geo_df (str): URL of geoJSON file with US counties geoshape
                boundaries
            zip_df (str): URL of ZIP codes and US counties by name
         """
        self.df = df
        self.geo_df = geo_df
        self.zip_df = zip_df

    def load_geoshapes(self):
        """
        Load geoshapes file from provided URL. Create column 'state_fips'
        to merge with US counties by ZIP code.

        Return:
            counties (DataFrame): geoshapes file with added column 'state_fips'
        """
        # set exceptions
        if not isinstance(self.geo_df, str):
            raise ValueError('"self.geo_df" must be of type string \
                             to a URL for a geoJSON file')

        counties = gpd.read_file(self.geo_df)
        counties['state_fips'] = counties['STATEFP'].astype('int')

        return counties

    def load_counties_zip(self):
        """
        Load ZIP codes and US counties by name. Create column 'NAME'
        to merge with geoshapes file.

        Return:
            counties_zip (DataFrame): ZIP codes and US counties with added
                column 'NAME'
        """
        # set exceptions
        if not isinstance(self.zip_df, str):
            raise ValueError('"self.zip_df" must be of type string \
                             to a URL for a county ZIP codes csv')
        
        counties_zip = pd.read_csv(self.zip_df)
        counties_zip['NAME'] = counties_zip['county']

        return counties_zip

    def merge_geoshapes_counties_zip(self):
        """
        Merge counties and counties_zip by common 'state_fips' and 'NAME'

        Return:
            counties_merge (DataFrame): merged DataFrame of counties
                and counties_zip
        """
        counties = self.load_geoshapes()
        counties_zip = self.load_counties_zip()

        counties_merge = counties.merge(counties_zip[['state_fips', 
                                                      'zipcode', 
                                                      'NAME']],
                                        on=['state_fips', 'NAME'],
                                        how='left')

        return counties_merge

    def zip_socioeconomic(self):
        """
        Load socioeconomic data by ZIP code and prepare to merge to
            counties_merge. Delete person_id and drop duplicates to 
            get aggregate data for each 3-digit ZIP code.

        Return:
            zip_socioeconomic_agg (DataFrame): contains socioeconmic data by 
                3-digit ZIP code
        """
        # set exceptions
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError('"self_df" must be a Pandas DataFrame')
        
        zip_socioeconomic_df = self.df
        zip_socioeconomic_agg = zip_socioeconomic_df.drop(
                                    columns=['person_id', 
                                             'observation_datetime'])
        zip_socioeconomic_agg = zip_socioeconomic_agg.drop_duplicates()

        return zip_socioeconomic_agg

    def merge_county_socioeconomic(self):
        """
        Merge county_merge and zip_socioeconomic_agg based on 3-digit
            ZIP code.

        Return:
            counties_socioeconomic (DataFrame): full geoshapes file with socioeconmic data
                by 3-digit ZIP code
        """
        zip_socioeconomic_agg = self.zip_socioeconomic()
        counties_merge = self.merge_geoshapes_counties_zip()

        # get 3-digit ZIP codes
        counties_merge['zip3'] = counties_merge['zipcode'].apply(
                                    lambda x: str(x)[0:3])
        zip_socioeconomic_agg['zip3'] = zip_socioeconomic_agg['zip_code'].apply(
                                            lambda x: x[0:3])

        # merge county_merge and zip_socioeconomic_agg
        counties_socioeconomic = counties_merge.merge(zip_socioeconomic_agg, 
                                                      on='zip3', 
                                                      how='left')
        counties_socioeconomic = counties_socioeconomic.drop_duplicates(
                                    subset='AFFGEOID')

        return counties_socioeconomic
