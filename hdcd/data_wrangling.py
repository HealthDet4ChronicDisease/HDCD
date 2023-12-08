"""
This Python script defines a class for data wrangling the
All of US dataset.

This script requires `numpy`, `pandas`, and `geopandas` within
the Python environment you are running this in.

The class accepts Pandas DataFrames and zip files of geoJSON.
The class consists of functions:
    * load_geoshapes
    * load_counties_zip
    * merge_geoshapes_counties_zip
    * zip_socioeconomic
    * merge_county_socioeconomic

This script can be imported as a module
"""
import os

import numpy as np
import pandas as pd
import geopandas as  gpd

class AoU():
    """
    This class consists of multiple functions to wrangle and clean
    the All of US dataset to produce interactive visualizations.
    """
    def __init__(self, df, geo_df, zip_df):
        """
        This function initializes objects to be passed in the class.

        Args:
            df (Pandas DataFrame): All of US ZIP code and socioeconomic
                dataset
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

        counties_merge = counties.merge(counties_zip[['state_fips', 'zipcode', 'NAME']],
                                        on=['state_fips', 'NAME'],
                                        how='left')

        return counties_merge

    def zip_socioeconomic(self):
        """
        Load socioeconomic data by ZIP code and prepare to merge to
            counties_merge

        Return:
            zip_socioeconomic_agg (DataFrame): contains socioeconmic data by ZIP code
        """
        zip_socioeconomic_df = self.df
        zip_socioeconomic_agg = zip_socioeconomic_df.drop(columns=['person_id', 'observation_datetime'])
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
        counties_merge['zip3'] = counties_merge['zipcode'].apply(lambda x: str(x)[0:3])
        zip_socioeconomic_agg['zip3'] = zip_socioeconomic_agg['zip_code'].apply(lambda x: x[0:3])

        # merge county_merge and zip_socioeconomic_agg
        counties_socioeconomic = counties_merge.merge(zip_socioeconomic_agg, on='zip3', how='left')
        counties_socioeconomic = counties_socioeconomic.drop_duplicates(subset='AFFGEOID')

        return counties_socioeconomic
