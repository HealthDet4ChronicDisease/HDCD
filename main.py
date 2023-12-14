"""
This Python script runs the Health Data Analysis modules for interactive
visualziations within this GitHub repository.
    * Data Wrangling
    * Summary Statistics
    * Plots

This script requires the following packages within the Python environment
you are running in:
    * NumPy
    * Pandas
    * GeoPandas
    * Altair
    * SciPy
"""

import argparse

import pandas as pd

from hdcd.data_wrangling import AoU_socioeconomic, AoU_conditions
from hdcd.plot import plot_corr, plot_geomap, plot_longitudinal_change, \
plot_geomap_socioeconomic, plot_geomap_conditions
from hdcd.summary import data_summary, variable_summary
from config import *

# define arguments
parser = argparse.ArgumentParser(description="Options for visualizations")

parser.add_argument('--plot_longitudinal', default=False,
                    action="store_true",
                    help='Set argument for longitudinal plot')
parser.add_argument('--plot_correlation', default=False,
                    action='store_true',
                    help='Set argument for correlation plot')
parser.add_argument('--plot_geomap',
                    choices=['socioeconomic', 'conditions', 'geomap'],
                    help='GeoMap type to visualize')
parser.add_argument('--summary_statistics',
                    choices=['data', 'variable'],
                    help='Summary statistics to run')
args = parser.parse_args()

"""
Required arguments for AoU_socioeconomic class
    df (DataFrame) from SQL query in All of US workspace
    geo_df (str): recommended URL below for geoshapes file of US counties
    zip_df (str): recommended URL for US counties by name and ZIP code
"""

# run AoU_socioeconomic data wrangling to get merged counties geoshapes \
# file and socioeconomic data
def main():
    """
    The main function. Call python main.py with arguments --argument to work.
    This function mainly served as a test for All of Us data and is integrated
    with CDI and 500 places data.

    For more information, check the four arguments:

    --plot_longitudinal
    --plot_correlation
    --plot_geomap
    --summary_statistics

    """
    if args.plot_geomap == 'socioeconomic':
        # df = <obtain from All of US SQL query 'zip_socioeconomic'>
        # THIS WILL NOT RUN LOCALLY
        geo_df = 'https://gist.githubusercontent.com/sdwfrost/\
d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/\
counties.geojson'
        county_df = 'https://raw.githubusercontent.com/\
scpike/us-state-county-zip/master/geo-data.csv'

        AoU_socioeconomic_wrangler = AoU_socioeconomic(df=df,
                                                       geo_df=geo_df,
                                                       county_df=county_df)
        counties_socioeconomic = AoU_socioeconomic_wrangler.merge_county_socioeconomic()
        plot_geomap_socioeconomic(dataframe=counties_socioeconomic)
    elif args.plot_geomap == 'geomap':
        dataframe = pd.read_csv("./data/cdi_dummy.csv")
        plot_geomap(variable=GEOMAP_VAR,
                    datatype=GEOMAP_DATATYPE,
                    stratification=GEOMAP_STRATIFICATION,
                    dataframe=dataframe,
                    color_scheme=GEOMAP_COLOR,
                    width = 'container')
    elif args.plot_geomap == 'conditions':
        conditions_df = pd.read_csv(CONDITIONS)
        observations_df = pd.read_csv(OBSERVATIONS)
        geo_df = 'https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d1759\
98ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson'
        county_df = 'https://raw.githubusercontent.com/scpike/us-state-county\
-zip/master/geo-data.csv'
        AoU_conditions_wrangler = AoU_conditions(conditions_df=conditions_df,
                                                 observations_df=observations_df,
                                                 county_df=county_df,
                                                 geo_df=geo_df)
        conditions_counts = AoU_conditions_wrangler.counties_groupby_count()
        plot_geomap_conditions(conditions_counts)
    else:
        print("Socioeconomic geomap was not selected for visualization.")

    if args.plot_correlation:
        dataframe = pd.read_csv("./data/cdi_dummy.csv")
        plot_corr(sod=CORR_SOD,
                  health_outcome=CORR_HEALTH_OUTCOME,
                  stratification=CORR_STRATIFICATION,
                  dataframe=dataframe,
                  print_corr=True)

    if args.plot_longitudinal:
        dataframe = pd.read_csv("./data/cdi_dummy.csv")
        plot_longitudinal_change(variable=LONG_VAR,
                                location=LONG_LOCATION,
                                stratification=LONG_STRATIFICATION,
                                dataframe=dataframe)

    if args.summary_statistics == 'data':
        dataframe = pd.read_csv("./data/cdi_dummy.csv")
        data_summary(dataframe=dataframe)
    elif args.summary_statistics == 'variable':
        dataframe = pd.read_csv("./data/cdi_dummy.csv")
        variable_summary(dataframe=dataframe, variable=SUMMARY_VAR)

if __name__ == "__main__":
    # raise argparse error if no parameters passed
    if not (args.plot_geomap or args.plot_correlation
            or args.plot_longitudinal or args.summary_statistics):
        parser.error('No visualization or summary statistics selected, \
please specify at least one.')
    else:
        main()
