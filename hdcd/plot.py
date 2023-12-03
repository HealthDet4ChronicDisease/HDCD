"""
Plotting module
"""

import pandas as pd
import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt
import altair as alt

import warnings
warnings.filterwarnings("ignore")

### --- TODO ----###
### Add __all__ to the import * in __init__
### Add print functions in vocab variable defining printing of correlation
### Add correlation coefficient selection Parameters
### Remove "US" from all plots with Locations

__all__ = ['plot_corr',"plot_geomap","plot_longitudinal_change"]

def plot_corr(sod,
             health_outcome,
             location,
             stratification,
             df):

    """
    Function to plot the correlation of two variables in a scatterplot. Implementation based on altair (alt).

    Parameters:
    @sod: string variable drawn from the [Question] column of the dataframe
    @health_outcome: string variable drawn from the [LocationDesc] column of the dataframe
    @stratification: string variable drawn from the [StratificationCategory1] column
    @output: an interactive pointplot of longitudinal change with respect to @variable
    @return: an alt.layer() object

    """

    data_analysis = df[(df["Question"] == sod) & (df["StratificationCategory1"] == stratification)]
    data_analysis["DataValue"] = data_analysis["DataValue"].astype(float)
    #print(data_analysis["DataValueType"].unique())

    v1 = data_analysis.groupby(["LocationAbbr","DataValueType"])["DataValue"].mean()
    v1 = pd.DataFrame(v1).reset_index().pivot(index = "LocationAbbr", columns = "DataValueType", values = 'DataValue')
    v1.columns = [sod + " - " + x for x in v1.columns]
    x_col = list(v1.columns)

    data_analysis = df[(df["Question"] == health_outcome) & (df["StratificationCategory1"] == stratification)]
    data_analysis["DataValue"] = data_analysis["DataValue"].astype(float)

    v2 = data_analysis.groupby(["LocationAbbr","DataValueType"])["DataValue"].mean()
    v2 = pd.DataFrame(v2).reset_index().pivot(index = "LocationAbbr", columns = "DataValueType", values = 'DataValue')
    v2.columns = [health_outcome + " - " + x for x in v2.columns]
    y_col = list(v2.columns)

    dfplot = v1.join(v2).reset_index()

    chart = alt.hconcat()
    #plotlist = []
    for xvar in x_col:
        for yvar in y_col:
            plot = alt.Chart(dfplot).mark_circle().encode(
            alt.X(xvar+":Q",scale=alt.Scale(zero=False)),
            alt.Y(yvar+":Q",scale=alt.Scale(zero=False)),
            tooltip=['LocationAbbr',xvar,yvar]
            )
            chart |= plot
            #plotlist.append(plot)
    return chart.interactive()


def plot_geomap(variable,
                datatype,
                df):
    """
    Plot a longitudinal geomap (of the United States) distribution of @variable, with unit in @datatype, given @df.

    Parameters
    @variable: str, a variable to lookup from the [Question] column of data, used to generate the plot,
    the [DataValue] column of the @df should be numeric.
    @datatype: str, the unit of the @variable. User can lookup the @datatype from the [DataValueType] column
    of the @df. Or user are recommended to use the variable_summary() function to check the DataValueType.
    @df: pd.DataFrame, the dataframe used to generate the plot, must be formatted and contains required columns,
    including ["YearStart","Question","DataValue","DataValueType"].
    """
    # set up id map
    from vega_datasets import data
    pop = data.population_engineers_hurricanes()
    state2id = dict(zip(pop["state"],
                        pop["id"]))

    dfplot = df[df["Question"] == variable]
    dfplot["id"] = [int(state2id[x]) if x in state2id else np.nan for x in dfplot["LocationDesc"]]

    # stratification
    stratification = 'Overall'
    dfplot = dfplot[dfplot["StratificationCategory1"] == stratification]

    # datatype
    dfplot = dfplot[dfplot["DataValueType"] == datatype]
    dfplot["DataValue"] = dfplot["DataValue"].astype(float)

    dfplot.dropna(subset = ["id"],inplace=True)
    dfplot["id"] = dfplot["id"].astype(int)

    # plot session
    # make slider bar
    select_year = alt.binding_range(min=dfplot["YearStart"].min(),
                  max=dfplot["YearStart"].max(),
                  step=1, name="YearStart")
    slider_selection = alt.selection_point(bind=select_year, fields=['YearStart'])

    states = alt.topo_feature(data.us_10m.url, feature='states')

    variable_list = ['DataValue',"YearStart","LocationDesc","LocationAbbr"]

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=500,
        height=300
    )

    # the tricky part is that if it is longitudinal, the map should be using the dfplot to lookup states
    # not the other way. Since if using states (the map itself) and lookup dfplot, the id would only identify
    # one specific year's status, and ignores the other years

    foreground = alt.Chart(dfplot).mark_geoshape().encode(
        color=alt.Color(
                "DataValue:Q", scale=alt.Scale(scheme="bluepurple",
                                               #domainMid = 0,
                                               domainMax = dfplot["DataValue"].max(),
                                               domainMin = dfplot["DataValue"].min()),
            ),
        tooltip=['LocationDesc:N', 'YearStart:Q', 'DataValue:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(states, 'id', ["id","type","properties","geometry"])
    ).properties(
        width=500,
        height=300
    ).project(
        type='albersUsa'
    ).add_selection(
        slider_selection
                    ).transform_filter(
        slider_selection,
    )
    return background + foreground


def plot_longitudinal_change(variable,
                             location,
                             stratification ,
                             df):

    """
    Plot a longitudinal lineplot of @variable, with unit in @datatype at different panels, given @df.

    Parameters:

    @variable: string variable drawn from the [Question] column of the dataframe
    @location: string variable drawn from the [LocationDesc] column of the dataframe
    @stratification: string variable drawn from the [StratificationCategory1] column
    @output: an interactive pointplot of longitudinal change with respect to @variable
    @return: an alt.layer() object

    """

    dfplot = df[(df["LocationDesc"] == location) & (df["Question"] == variable)]
    tmp = dfplot[dfplot["StratificationCategory1"] == stratification]

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
