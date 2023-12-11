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
    * SciPy
"""
import os
import sys
import argparse

from hdcd.data_wrangling import AoU_socioeconomic
from hdcd.plot import *
from hdcd.summary import *

# define arguments
parser = argparse.ArgumentParser(description="Options for visualizations")

parser.add_argument('--plot_longitudinal', default=False, 
                    action="store_true", 
                    help='Set argument for longitudinal plot')
parser.add_argument('--plot_correlation', default=False, 
                    action='store_true', 
                    help='Set argument for correlation plot')
parser.add_argument('--plot_geomap', 
                    choices=['socioeconomic', 'location', 'geomap'],
                    help='GeoMap type to visualize')
parser.add_argument('--summary_statistics', 
                    choices=['data', 'summary'], 
                    help='Summary statistics to run')
args = parser.parse_args()

"""
Required arguments for AoU_socioeconomic class
    df (DataFrame) from SQL query in All of US workspace
    geo_df (str): recommended URL below for geoshapes file of US counties
    zip_df (str): recommended URL for US counties by name and ZIP code
"""
# df = <obtain from All of US SQL query 'zip_socioeconomic'>
geo_df = 'https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson'
zip_df = 'https://raw.githubusercontent.com/scpike/us-state-county-zip/master/geo-data.csv'

# run AoU_socioeconomic data wrangling to get merged counties geoshapes \ 
# file and socioeconomic data
def main():
    if args.plot_geomap == 'socioeconomic':
        counties_socioeconomic = AoU.merge_county_socioeconomic(df=df, geo_df=geo_df, zip_df=zip_df)
        plot_geomap()
    elif args.plot_geomap == 'location':
        plot_geomap_by_location()
    elif args.plot_geomap == 'geomap':
        plot_geomap()
    else:
        print("Socioeconomic geomap was not selected for visualization.")

    if args.plot_correlation:
        plot_corr()

    if args.plot_longitudinal:
        plot_longitudinal_change()

    if args.summary_statistics == 'data':
        data_summary()
    elif args.summary_statistics == 'variable':
        variable_summary()
    

if __name__ == "__main__":
    if not (args.plot_geomap or args.plot_correlation 
            or args.plot_longitudinal or args.summary_statistics):
        parser.error('No visualization selected, add one type')
    else:
        print("The selected visualizations are ready.")
    