"""
This Python script contains adjustable parameters for defining
variables for social determinants of health (SDOH) and conditions.

For the visualization you wish to produce, type in the variable
for that section.

These parameters are imported and passed to main.py.
"""

"""
Summary Statistics
"""
# variable to be passed to variable_summary
SUMMARY_VAR = 'Binge drinking frequency among adults aged >= 18 years who binge drink'

"""
Correlation Plot
"""
CORR_SOD = 'Binge drinking frequency among adults aged >= 18 years who binge drink'
CORR_HEALTH_OUTCOME = 'Life expectancy at birth'
CORR_STRATIFICATION = 'overall'

"""
CDI GeoMap
plot_geomap
"""
GEOMAP_VAR = "Binge drinking frequency among adults aged >= 18 years who binge drink"
GEOMAP_DATATYPE = "Age-adjusted Mean"
GEOMAP_STRATIFICATION = "Overall"
GEOMAP_COLOR ='bluepurple'
GEOMAP_WIDTH ='container'

"""
Longitudinal Time-series
plot_longitudinal_change
"""
LONG_VAR = "Binge drinking frequency among adults aged >= 18 years who binge drink"
LONG_LOCATION = "Arkansas"
LONG_STRATIFICATION = "Gender"

"""
Conditions GeoMap
plot_geomap_conditions
    * links to dummy data csv
"""
CONDITIONS = './data/condition_data.csv'
OBSERVATIONS = './data/observation_data.csv'