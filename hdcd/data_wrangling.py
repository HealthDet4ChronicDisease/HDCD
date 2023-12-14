"""
This Python script defines clasess for data wrangling the
All of US dataset.
    * AoU_socioeconomic: county-level socioeconomic data
    * AoU_conditions: aggregated county-level conditions counts

This script requires `numpy`, `pandas`, and `geopandas` within
the Python environment you are running this in.

The AoU_socioeconomic class accepts Pandas DataFrames, csv files, and
    zip files of geoJSON. The class consists of functions:
    * load_geoshapes
    * load_counties_zip
    * merge_geoshapes_counties_zip
    * zip_socioeconomic
    * merge_county_socioeconomic

The AoU_conditions class accepts Pandas DataFrames and csv files.
    The class consists of functions:
    * load_counties_zip
    * threshold_conditions
    * observation_zip
    * merge_conditions_observation
    * groupby_count

The classes can be imported as modules.
"""
import os

import numpy as np
import pandas as pd
import geopandas as  gpd

# recommended geoshapes file and ZIP codes for US counties file
geo_df = 'https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson'
county_df = 'https://raw.githubusercontent.com/scpike/us-state-county-zip/master/geo-data.csv'

class AoU_socioeconomic():
    """
    This class consists of multiple functions to wrangle and clean
    the All of US dataset to produce interactive visualizations
    specifically for county level socioeconomic data, as defined by
    All of Us.
    """
    def __init__(self, df, geo_df, county_df):
        """
        This function initializes objects to be passed in the class.

        Args:
            df (DataFrame): All of US ZIP code and socioeconomic
                DataFrame to be passed from SQL query
            geo_df (str): URL of geoJSON file with US counties geoshape
                boundaries
            county_df (str): URL of ZIP codes and US counties by name
         """
        self.df = df
        self.geo_df = geo_df
        self.county_df = county_df

    def load_geoshapes(self):
        """
        Load geoshapes file from provided URL. Create column 'state_fips'
        to merge with US counties by ZIP code.

        Return:
            counties (DataFrame): geoshapes file with added column 'state_fips'
        """
        # set exceptions
        if not isinstance(self.geo_df, str):
            raise ValueError('"geo_df" must be of type string \
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
        if not isinstance(self.county_df, str):
            raise ValueError('"county_df" must be of type string \
                             to a URL for a county ZIP codes csv')

        counties_zip = pd.read_csv(self.county_df)
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
                                                      'NAME',
                                                      'state']],
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
            raise ValueError('"df" must be a Pandas DataFrame')

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

class AoU_conditions():
    """
    This class consists of multiple functions to wrangle and clean
    the All of US dataset to produce interactive visualizations
    specifically for county level conditions data, as defined by
    All of Us.
    """
    def __init__(self, conditions_df, observations_df, county_df, geo_df):
        """
        This function initializes objects to be passed in the class.

        Args:
            conditions_df (DataFrame): All of US conditions data to be
                passed from SQL query
            observations_df (DataFrame): All of US observations data
                with ZIP code to be passed from SQL query
            county_df (str): URL of ZIP codes and US counties by name
            geo_df (str): URL of geoJSON file with US counties geoshape
                boundaries
         """
        self.conditions_df = conditions_df
        self.observations_df = observations_df
        self.county_df = county_df
        self.geo_df = geo_df

    def load_counties_zip(self):
        """
        Load ZIP codes and US counties by name. Create column 'NAME'
        to merge with geoshapes file.

        Return:
            counties_zip (DataFrame): ZIP codes and US counties with added
                column 'zip3'
        """
        # set exceptions
        if not isinstance(self.county_df, str):
            raise ValueError('"county_df" must be of type string \
                             to a URL for a county ZIP codes csv')

        counties_zip = pd.read_csv(self.county_df)
        counties_zip['zip3'] = counties_zip['zipcode'].apply(lambda x: str(x)[0:3]).astype('int')

        return counties_zip

    def threshold_conditions(self):
        """
        Threshold conditions of interest so that only those with at least
            a prevalence of 100k are included for visualization.

        Return:
            conditions_df_threshold (DataFrame): conditions with at least
                a prevalence of 100k
        """
        # threshold at least 10k
        conditions_df_threshold = self.conditions_df[self.conditions_df.groupby('standard_concept_name')['standard_concept_name'].transform('size')>100000]

        # keep columns for merging to counties_zip
        conditions_df_threshold = conditions_df_threshold[['person_id', 'standard_concept_name', 'condition_start_datetime']]
        conditions_df_threshold['condition_start_datetime'] = pd.to_datetime(conditions_df_threshold['condition_start_datetime'])

        return conditions_df_threshold

    def observation_zip(self):
        """
        Extract participant level 3-digit zip codes from observation dataset

        Return:
            zip_df (DataFrame): participant level 3-digit zip codes
        """
        # extract 3-digit zip codes to DataFrame
        if not isinstance(self.observations_df, pd.DataFrame):
            raise ValueError('"observations_df" must be a Pandas DataFrame')

        postal_code = self.observations_df.loc[self.observations_df.standard_concept_name == 'Postal code [Location]']
        postal_code['observation_datetime'] = pd.to_datetime(postal_code['observation_datetime'])

        zip_list = []

        for i,row in postal_code.iterrows():
            tmp = dict()

            tmp['person_id'] = int(row.person_id)
            tmp['zip'] = row.value_as_string
            tmp['datetime'] = row.observation_datetime
            zip_list.append(tmp)

        zip_df = pd.DataFrame(zip_list)

        return zip_df

    def merge_conditions_observation(self):
        """
        Merge conditions to participant level 3-digit zip codes

        Return:
            conditions_zip_unique_county (DataFrame): participant level
                3-digit ZIP code conditions by year and month
        """
        zip_df = self.observation_zip()
        conditions_df_threshold = self.threshold_conditions()
        counties_zip = self.load_counties_zip()

        # merge conditions to participants on person_id keeping first match
        conditions_zip_unique = zip_df.merge(conditions_df_threshold.drop_duplicates(['person_id', 'standard_concept_name']),
                                             on='person_id',
                                             how='inner')

        # get 3-digipt ZIP codes from US county ZIP file
        counties_zip['zip3'] = counties_zip['zipcode'].apply(lambda x: str(x)[0:3]).astype('int')

        # merge conditions_zip_unique to counties_zip on 3-digit ZIP code
        conditions_zip_unique['zip3'] = conditions_zip_unique['zip'].apply(lambda x: x[0:3]).astype('int')
        conditions_zip_unique_county = conditions_zip_unique.merge(counties_zip, on='zip3', how='inner')

        # extract year and month for condition_start_datetime
        conditions_zip_unique_county['year'] = pd.DatetimeIndex(conditions_zip_unique_county['condition_start_datetime']).year
        conditions_zip_unique_county['month'] = pd.DatetimeIndex(conditions_zip_unique_county['condition_start_datetime']).month

        return conditions_zip_unique_county

    def groupby_count(self):
        """
        Count total participants for a condition in each ZIP code
            stratified by datetime year and month

        Return:
            conditions_zip_datetime_counts (DataFrame): total participants
                with conditions in ZIP code by year and month
        """
        conditions_zip_unique_county = self.merge_conditions_observation()

        conditions_zip_datetime_counts = conditions_zip_unique_county.groupby(by=['zipcode',
                                                                                  'year',
                                                                                  'month',
                                                                                  'standard_concept_name'])['person_id'].count()

        return pd.DataFrame(conditions_zip_datetime_counts)

    def merge_counties_groupby(self):
        """
        Count total participants for a condition in each county
            stratified by year.

        Return:
            conditions_counts (DataFrame): total counts for each condition
                stratified by county and year
        """
        conditions_zip_datetime_counts = self.groupby_count()
        counties = gpd.read_file(self.geo_df)

        countyname2geoid = dict(zip(counties["NAME"],
                                counties["GEOID"].astype(int)))
        conditions_zip_datetime_counts["id"] = [countyname2geoid[x] if x in countyname2geoid else np.nan for x in conditions_zip_datetime_counts["county"].tolist()]

        conditions_counts = conditions_zip_datetime_counts.groupby(["standard_concept_name","county","year","state_abbr","id"])["person_id"].nunique().reset_index()

        conditions_counts.rename(columns = {"person_id":"counts"},inplace=True)
        conditions_counts.dropna(subset = ["id"],inplace=True)
        conditions_counts["id"] = mentalDisorder_counts["id"].astype(int)

        return conditions_counts
