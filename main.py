"""
This Python script runs the Health Data Analysis modules for interactive
visualziations within this GitHub repository.
    * Data Wrangling
    * Summary Statistics
    * Plots

These modules require the following packages within the Python environment
you are running in:
    * NumPy
    * Pandas
    * GeoPandas
    * Altair
"""
import os
import sys

from hdcd.data_wrangling import AoU_socioeconomic
from hdcd.plot import *
from hdcd.summary import *

# define necessary inputs for AoU_socioeconomic
# recommended geoshapes file and ZIP codes for US counties file
# df = <obtain from All of US SQL query 'zip_socioeconomic'>
geo_df = 'https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson'
zip_df = 'https://raw.githubusercontent.com/scpike/us-state-county-zip/master/geo-data.csv'

# run AoU_socioeconomic data wrangling to get merged counties geoshapes \ 
# file and socioeconomic data
counties_socioeconomic = AoU.merge_county_socioeconomic(df=df, geo_df=geo_df, zip_df=zip_df)