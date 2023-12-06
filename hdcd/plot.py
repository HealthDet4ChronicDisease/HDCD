"""
Plotting module
"""
import warnings

import pandas as pd
import numpy as np
import scipy.stats as sp
import altair as alt

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
             location,
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
    dataframe = dataframe[dataframe["LocationAbbr"] != "US"]

    data_analysis = dataframe[(dataframe["Question"] == sod) \
    & (dataframe["StratificationCategory1"] == stratification)]

    # coerce into numeric
    data_analysis["DataValue"] = data_analysis["DataValue"].astype(float)

        # set exceptions
    if all( not str(x).replace(".","").isdigit() \
        for x in data_analysis["DataValue"].tolist()):
        raise TypeError("All value in the DataValue column can not be coerced \
into numeric or contains NAs, try to clean it before analyzing.")

    sod_var = data_analysis.groupby(["LocationAbbr",
                                     "DataValueType"])["DataValue"].mean()

    sod_var = pd.DataFrame(sod_var).reset_index().pivot(index = "LocationAbbr",
                                              columns = "DataValueType",
                                              values = 'DataValue')

    sod_var.columns = [sod + " - " + x for x in sod_var.columns]
    x_col = list(sod_var.columns)

    data_analysis = dataframe[(dataframe["Question"] == health_outcome) \
    & (dataframe["StratificationCategory1"] == stratification)]
    data_analysis["DataValue"] = data_analysis["DataValue"].astype(float)

    # set exceptions
    if all( not str(x).replace(".","").isdigit() \
        for x in data_analysis["DataValue"].tolist()):
        raise TypeError("All value in the DataValue column can not be coerced \
into numeric or contains NAs, try to clean it before analyzing.")

    outcome_var = data_analysis.groupby(["LocationAbbr",
                                         "DataValueType"])["DataValue"].mean()

    outcome_var = pd.DataFrame(outcome_var).reset_index().pivot(index = "LocationAbbr",
                                              columns = "DataValueType",
                                              values = 'DataValue')
    outcome_var.columns = [health_outcome + " - " + x for x in outcome_var.columns]
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
                dataframe,
                color_scheme = "bluepurple",
                width = 1280,
                height = 720):
    """
    Plot a longitudinal geomap (of the United States) distribution of @variable,
with unit in @datatype, given @dataframe.

    Parameters
    @variable: str, a variable to lookup from the [Question] column of data,
used to generate the plot,the [DataValue] column of the @dataframe should be numeric.
    @datatype: str, the unit of the @variable. User can lookup the @datatype
from the [DataValueType] column of the @dataframe. Or user are recommended to use
the variable_summary() function to check the DataValueType.
    @dataframe: pd.DataFrame, the dataframe used to generate the plot, must be
formatted and contains required columns, including
["YearStart","Question","DataValue","DataValueType"].
    """
    # set up id map
    from vega_datasets import data
    pop = data.population_engineers_hurricanes()
    state2id = dict(zip(pop["state"],
                        pop["id"]))

    dataframeplot = dataframe[dataframe["Question"] == variable]
    dataframeplot["id"] = [int(state2id[x]) \
    if x in state2id else np.nan for x in dataframeplot["LocationDesc"]]

    # stratification
    stratification = 'Overall'
    dataframeplot = dataframeplot[dataframeplot["StratificationCategory1"] \
    == stratification]

    # datatype
    dataframeplot = dataframeplot[dataframeplot["DataValueType"] == datatype]
    dataframeplot["DataValue"] = dataframeplot["DataValue"].astype(float)

    dataframeplot.dropna(subset = ["id"],inplace=True)
    dataframeplot["id"] = dataframeplot["id"].astype(int)

    # plot session
    # make slider bar
    select_year = alt.binding_range(min=dataframeplot["YearStart"].min(),
                  max=dataframeplot["YearStart"].max(),
                  step=1, name="YearStart")
    slider_selection = alt.selection_point(bind=select_year,
                                           fields=['YearStart'])

    states = alt.topo_feature(data.us_10m.url, feature='states')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=width,
        height=height
    )

    foreground = alt.Chart(dataframeplot).mark_geoshape().encode(
        color=alt.Color(
                "DataValue:Q",
                scale=alt.Scale(scheme=color_scheme,
                                domainMax = dataframeplot["DataValue"].max(),
                                domainMin = dataframeplot["DataValue"].min()),
            ),
        tooltip=['LocationDesc:N', 'YearStart:Q', 'DataValue:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(states, 'id', ["id",
                                            "type",
                                            "properties",
                                            "geometry"])
    ).properties(
        width=width,
        height=height
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
                            width = 500,
                            height = 300):

    """
    Plot a longitudinal geomap (of the United States) distribution of @variable,
    with unit in @datatype, given @dataframe.
    This plot is made based on the longitude and latitude of the dataset.

    Parameters
    @variable: str, a variable to lookup from the [Question] column of data, \
used to generate the plot, the [DataValue] column of the @dataframe should be numeric.
    @datatype: str, the unit of the @variable. User can lookup the @datatype \
from the [DataValueType] column of the @dataframe. Or user are recommended to use the \
variable_summary() function to check the DataValueType.
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
        width=width,
        height=height,
    )

    points = alt.Chart(dataframe).mark_circle().encode(
        longitude=longitude+':Q',
        latitude=latitude+':Q',
        color=alt.Color(
               "DataValue:Q", scale=alt.Scale(scheme=color_scheme,
               #domainMid = 0,
               domainMax = dataframe["DataValue"].max(),
               domainMin = dataframe["DataValue"].min()),
                ),
            tooltip=['LocationDesc:N',
                     'YearStart:Q',
                     'DataValue:Q',
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

    dataframeplot = dataframe[(dataframe["LocationDesc"] == location) \
    & (dataframe["Question"] == variable)]
    tmp = dataframeplot[dataframeplot["StratificationCategory1"] \
    == stratification]

    domain = list(tmp["Stratification1"].unique())
    colors = alt.Scale(
      domain= domain,
    )

    line = alt.Chart().mark_line().encode(
        alt.X("YearStart:O",),
        alt.Y("DataValue:Q",scale=alt.Scale(zero=False)),
        alt.Color('Stratification1:N', scale=colors),
        tooltip=["YearStart","DataValue",'Stratification1']
    )

    points = alt.Chart().mark_point().encode(
        alt.X("YearStart:O",),
        alt.Y("DataValue:Q",scale=alt.Scale(zero=False)),
        alt.Color('Stratification1:N', scale=colors),
        tooltip=["YearStart","DataValue",'Stratification1'])

    cis = alt.Chart().mark_line().encode(
        alt.X("YearStart:O",),
        alt.Y("LowConfidenceLimit:Q",scale=alt.Scale(zero=False)),
        alt.Y2("HighConfidenceLimit:Q"),
        alt.Color('Stratification1:N', scale=colors),
        tooltip=["YearStart","DataValue",'Stratification1'])

    return alt.layer(points, cis, line).facet(
      data=tmp,
      column='DataValueType:N'
    ).resolve_scale(
        x='independent',
        y='independent')
