"""
Plotting module
"""
import warnings

import pandas as pd
import numpy as np
import scipy.stats as sp
import altair as alt
import geopandas as gpd

warnings.filterwarnings("ignore")

### --- TODO ----###
### Add __all__ to the import * in __init__
### Add print functions in vocab variable defining printing of correlation
### Add correlation coefficient selection Parameters
LOC_SHORT = "LocationAbbr"
LOC_LONG = "LocationDesc"
D_VALUE = "DataValue"
STRAT_SHORT = "Stratification1"
STRAT_LONG = "StratificationCategory1"
D_TYPE = "DataValueType"
YEAR = "YearStart"

__all__ = ['plot_corr',"plot_geomap","plot_longitudinal_change"]

def plot_corr(sod,
             health_outcome,
             stratification,
             dataframe,
             print_corr=False):

    """
    Function to plot the correlation of two variables in a scatterplot.
Implementation based on altair (alt).

    Parameters:
    @sod: string variable drawn from the [Question] column of the dataframe
    @health_outcome: string variable drawn from the [LocationDesc] column of
the dataframe
    @stratification: string variable drawn from the [StratificationCategory1]
column
    @output: an interactive pointplot of longitudinal change with respect to
@variable
    @return: an alt.layer() object

    """
    dataframe = dataframe[dataframe[LOC_SHORT] != "US"]

    # set exceptions
    if sod not in set(dataframe["Question"]):
        raise NameError(f"{sod} not found in dataframe, check [Question] \
columns for available variable")

    if health_outcome not in set(dataframe["Question"]):
        raise NameError(f"{health_outcome} not found in dataframe, check \
[Question] columns for available variable")

#     if location not in set(dataframe[LOC_SHORT]):
#         raise NameError(f"{location} not found in dataframe, check \
# [LocationAbbr] columns for available sod variable")

    if stratification not in set(dataframe[STRAT_LONG]):
        raise NameError(f"{stratification} not found in dataframe, check \
[StratificationCategory1] columns for available sod variable")

    data_analysis = dataframe[(dataframe["Question"] == sod) \
    & (dataframe[STRAT_LONG] == stratification)]

    # set exceptions
    if all( not str(x).replace(".","").isdigit() \
        for x in data_analysis[D_VALUE].tolist()):
        raise TypeError("All value in the DataValue column can not be coerced \
into numeric or contains NAs, try to clean it before analyzing.")
    # coerce into numeric
    data_analysis[D_VALUE] = data_analysis[D_VALUE].astype(float)


    sod_var = data_analysis.groupby([LOC_SHORT,
                                     D_TYPE])[D_VALUE].mean()

    sod_var = pd.DataFrame(sod_var).reset_index().pivot(index = LOC_SHORT,
                                              columns = D_TYPE,
                                              values = 'DataValue')

    sod_var.columns = [sod + " - " + x for x in sod_var.columns]
    x_col = list(sod_var.columns)

    data_analysis = dataframe[(dataframe["Question"] == health_outcome) \
    & (dataframe[STRAT_LONG] == stratification)]

    # set exceptions
    if all( not str(x).replace(".","").isdigit() \
        for x in data_analysis[D_VALUE].tolist()):
        raise TypeError("All value in the DataValue column can not be coerced \
into numeric or contains NAs, try to clean it before analyzing.")

    data_analysis[D_VALUE] = data_analysis[D_VALUE].astype(float)

    outcome_var = data_analysis.groupby([LOC_SHORT,
                                         D_TYPE])[D_VALUE].mean()

    outcome_var = pd.DataFrame(outcome_var).reset_index().pivot(index = LOC_SHORT,
                                              columns = D_TYPE,
                                              values = 'DataValue')
    outcome_var.columns = [health_outcome \
        + " - " + x for x in outcome_var.columns]

    y_col = list(outcome_var.columns)

    dataframeplot = sod_var.join(outcome_var).reset_index()

    chart = alt.hconcat()
    #plotlist = []
    for xvar in x_col:
        for yvar in y_col:
            plot = alt.Chart(dataframeplot).mark_circle().encode(
            alt.X(xvar+":Q",scale=alt.Scale(zero=False)),
            alt.Y(yvar+":Q",scale=alt.Scale(zero=False)),
            tooltip=['LocationAbbr',xvar,yvar]
            )
            chart |= plot

            if print_corr:
                res = sp.stats.spearmanr(dataframeplot.dropna()[xvar],
                                   dataframeplot.dropna()[yvar])
                print(f'spearmanr correlation coefficient for \
[{xvar}] and [{yvar}]: {res} \n')

    return chart.interactive()


def plot_geomap(variable,
                datatype,
                stratification,
                dataframe,
                color_scheme = "bluepurple",
                width = 'container'):
                # height = 720):
    """
    Plot a longitudinal geomap (of the United States) distribution of @variable,
with unit in @datatype, given @dataframe.

    Parameters
    @variable: str, a variable to lookup from the [Question] column of data,
used to generate the plot,the [DataValue] column of the @dataframe should be \
numeric.
    @datatype: str, the unit of the @variable. User can lookup the @datatype
from the [DataValueType] column of the @dataframe. Or user are recommended to \
use the variable_summary() function to check the DataValueType.
    @dataframe: pd.DataFrame, the dataframe used to generate the plot, must be
formatted and contains required columns, including
["YearStart","Question","DataValue","DataValueType"].
    """
    # set up id map
    from vega_datasets import data
    pop = data.population_engineers_hurricanes()
    state2id = dict(zip(pop["state"],
                        pop["id"]))

    # set exceptions
    if variable not in set(dataframe["Question"]):
        raise NameError(f"{variable} not found in dataframe, check [Question] \
columns for available variable")

    if datatype not in set(dataframe[D_TYPE]):
        raise NameError(f"{datatype} not found in dataframe, check \
[DataValueType] columns for available variable")

    if stratification not in set(dataframe[STRAT_LONG]):
        raise NameError(f"{stratification} not found in dataframe, check \
[StratificationCategory1] columns for available variable")

    dataframeplot = dataframe[dataframe["Question"] == variable]
    dataframeplot["id"] = [int(state2id[x]) \
    if x in state2id else np.nan for x in dataframeplot[LOC_LONG]]

    # stratification
    dataframeplot = dataframeplot[dataframeplot[STRAT_LONG] \
    == stratification]

    # datatype
    if all( not str(x).replace(".","").isdigit() \
        for x in dataframeplot[D_VALUE].tolist()):
        raise TypeError("All value in the DataValue column can not be coerced \
into numeric or contains NAs, try to clean it before analyzing.")

    dataframeplot = dataframeplot[dataframeplot[D_TYPE] == datatype]
    dataframeplot[D_VALUE] = dataframeplot[D_VALUE].astype(float)

    dataframeplot.dropna(subset = ["id"],inplace=True)
    dataframeplot["id"] = dataframeplot["id"].astype(int)

    # plot session
    # make slider bar
    select_year = alt.binding_range(min=dataframeplot[YEAR].min(),
                  max=dataframeplot[YEAR].max(),
                  step=1, name=YEAR)
    slider_selection = alt.selection_point(bind=select_year,
                                           fields=['YearStart'])

    states = alt.topo_feature(data.us_10m.url, feature='states')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=width
        # height=height
    )

    foreground = alt.Chart(dataframeplot).mark_geoshape().encode(
        color=alt.Color(
                D_VALUE+":Q",
                scale=alt.Scale(scheme=color_scheme,
                                domainMax = dataframeplot[D_VALUE].max(),
                                domainMin = dataframeplot[D_VALUE].min()),
            ),
        tooltip=[LOC_LONG+":N", YEAR+":Q", D_VALUE+":Q"]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(states, 'id', ["id",
                                            "type",
                                            "properties",
                                            "geometry"])
    ).properties(
        width=width
        # height=height
    ).project(
        type='albersUsa'
    ).add_selection(
        slider_selection
                    ).transform_filter(
        slider_selection,
    )
    return background + foreground


def plot_geomap_by_location(variable,
                            datatype,
                            dataframe,
                            longitude = "longitude",
                            latitude = "latitude",
                            color_scheme = "bluepurple",
                            width = 'container'):
                            # height = 720):

    """
    Plot a longitudinal geomap (of the United States) distribution of @variable,
    with unit in @datatype, given @dataframe.
    This plot is made based on the longitude and latitude of the dataset.

    Parameters
    @variable: str, a variable to lookup from the [Question] column of data, \
used to generate the plot, the [DataValue] column of the @dataframe should be \
numeric.
    @datatype: str, the unit of the @variable. User can lookup the @datatype \
from the [DataValueType] column of the @dataframe. Or user are recommended to \
use the variable_summary() function to check the DataValueType.
    @dataframe: pd.DataFrame, the dataframe used to generate the plot, must be \
formatted and contains required columns,
    including ["YearStart","Question","DataValue","DataValueType"].
    """

    from vega_datasets import data

    states = alt.topo_feature(data.us_10m.url, feature='states')
    dataframe = dataframe[dataframe["Question"] == variable]

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=width
        # height=height,
    )

    points = alt.Chart(dataframe).mark_circle().encode(
        longitude=longitude+':Q',
        latitude=latitude+':Q',
        color=alt.Color(
               D_VALUE+":Q", scale=alt.Scale(scheme=color_scheme,
               #domainMid = 0,
               domainMax = dataframe[D_VALUE].max(),
               domainMin = dataframe[D_VALUE].min()),
                ),
            tooltip=[LOC_LONG+":N",
                     YEAR+":Q",
                     D_VALUE+":Q",
                     "Question:N",
                     "DataValueType:N"],

        size=alt.value(10),
    )

    return background + points


def plot_longitudinal_change(variable,
                             location,
                             stratification,
                             dataframe):

    """
    Plot a longitudinal lineplot of @variable, with unit in @datatype at \
different panels, given @dataframe.

    Parameters:

    @variable: string variable drawn from the [Question] column of the dataframe
    @location: string variable drawn from the [LocationDesc] column of the \
dataframe
    @stratification: string variable drawn from the [StratificationCategory1] \
column
    @output: an interactive pointplot of longitudinal change with respect to \
@variable
    @return: an alt.layer() object

    """

    dataframeplot = dataframe[(dataframe[LOC_LONG] == location) \
    & (dataframe["Question"] == variable)]
    tmp = dataframeplot[dataframeplot[STRAT_LONG] \
    == stratification]

    domain = list(tmp[STRAT_SHORT].unique())
    colors = alt.Scale(
      domain= domain,
    )

    line = alt.Chart().mark_line().encode(
        alt.X(YEAR+":O",),
        alt.Y(D_VALUE+":Q",scale=alt.Scale(zero=False)),
        alt.Color('Stratification1:N', scale=colors),
        tooltip=[YEAR,D_VALUE,STRAT_SHORT]
    )

    points = alt.Chart().mark_point().encode(
        alt.X(YEAR+":O",),
        alt.Y(D_VALUE+":Q",scale=alt.Scale(zero=False)),
        alt.Color('Stratification1:N', scale=colors),
        tooltip=[YEAR,D_VALUE,STRAT_SHORT])

    cis = alt.Chart().mark_line().encode(
        alt.X(YEAR+":O",),
        alt.Y("LowConfidenceLimit:Q",scale=alt.Scale(zero=False)),
        alt.Y2("HighConfidenceLimit:Q"),
        alt.Color('Stratification1:N', scale=colors),
        tooltip=[YEAR,D_VALUE,STRAT_SHORT])

    return alt.layer(points, cis, line).facet(
      data=tmp,
      column='DataValueType:N'
    ).resolve_scale(
        x='independent',
        y='independent')

def plot_geomap_socioeconomic(dataframe,
                              width='container'):
    """
    Plot a geomap of selected SDOH given @dataframe at the county level.
        * High school education (%)
        * Median income ($)
        * No health insurance (%)
        * Poverty (%)

    Parameters:

    @dataframe: counties_socioeconomic dataframe from data_wrangling.AoU_socioeconomic
    @return: an alt.Chart() object with geomap and encoded SDOH data
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError('"dataframe" must be a Pandas DataFrame')

    from vega_datasets import data
    alt.data_transformers.disable_max_rows()

    for sdoh in ['high_school_education',
                'median_income',
                'no_health_insurance',
                'poverty']:

        dataframe[sdoh] = dataframe[sdoh].astype('float')
        if sdoh == 'high_school_education':
            title = 'High School Education (%)'
            scheme = 'darkblue'
        elif sdoh == 'median_income':
            title = 'Median Income ($)'
            scheme = 'yelloworangered'
        elif sdoh == 'no_health_insurance':
            title = 'No Health Insurance (%)'
            scheme = 'lightgreyred'
        elif sdoh == 'poverty':
            title = 'Poverty (%)'
            scheme = 'lightmulti'

        counties = alt.topo_feature(data.us_10m.url, 'counties')

        background = alt.Chart(counties).mark_geoshape(
                fill='lightgray',
                stroke='white'
            ).project('albersUsa').properties(
                width=width,
                #height=760
            )

        sdoh_geomap = alt.Chart(dataframe, title=title).mark_geoshape(
                    stroke='white'
                    ).encode(
                color=alt.Color(sdoh+':Q',
                                scale=alt.Scale(scheme=scheme),
                                title=title),
                tooltip=[alt.Tooltip('county:N', title='County'),
                        alt.Tooltip('state_abbr:N', title='State'),
                        alt.Tooltip(sdoh+':Q', title=title, format='.2f')]
                    ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(counties, 'id',["id",
                                                 "type",
                                                 "properties",
                                                 "geometry"])
        ).project(
                        type='albersUsa'
                    ).properties(
                        width=width
        )

        sdoh_geomap = background + sdoh_geomap

        #sdoh_geomap.save(sdoh + '_geomap.html')

    return sdoh_geomap

def plot_geomap_conditions(dataframe, width='container'):
    """
    Plot a geomap of conditions given @dataframe.

    Parameters:

    @dataframe: conditions dataframe from data_wrangling.AoU_conditions
    @return: an alt.Chart() object with geomap and encoded conditions counts
    """
    from vega_datasets import data

    if dataframe.empty:
        raise ValueError(f"{dataframe} is empty, load a dataframe that is not empty.")

    alt.data_transformers.disable_max_rows()
    counties = gpd.read_file('https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson')

    countyname2geoid = dict(zip(counties["NAME"],
                            counties["GEOID"].astype(int)))

    dfplot = dataframe.copy()
    counties = alt.topo_feature(data.us_10m.url, 'counties')

    input_dropdown = alt.binding_select(options=list(dataframe["standard_concept_name"].unique()),
                                    name='Conditions')
    selection_dropdown = alt.selection_single(fields=['standard_concept_name'],
                                              bind=input_dropdown)

    background = alt.Chart(counties).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).project('albersUsa').properties(
            width=width,
            #height=760
        )

    select_year = alt.binding_range(min=dfplot["year"].min(),
                max=dfplot["year"].max(),
                step=1, name="year")
    slider_selection = alt.selection_point(bind=select_year,
                                        fields=['year'])

    input_dropdown = alt.binding_select(options=list(dfplot["standard_concept_name"].unique()),
                                    name='Conditions')
    selection_dropdown = alt.selection_single(fields=['standard_concept_name'],
                            bind=input_dropdown)

    foreground = alt.Chart(dfplot).mark_geoshape().encode(
        color='counts:Q',
        tooltip=["standard_concept_name:N",
                "year:Q",
                "county:N",
                "state_abbr:N",
                "counts:Q"]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(counties, 'id',["id",
                                             "type",
                                             "properties",
                                             "geometry"])
    ).project(
        type='albersUsa'
    ).properties(
            width=width,
            #height=760
    ).add_selection(
            selection_dropdown,
            slider_selection
                        ).transform_filter(
            selection_dropdown,
    ).transform_filter(
            slider_selection,
    )

    conditions_geomap = background + foreground
    #conditions_geomap.save('conditions_geomap.html')

    return conditions_geomap
