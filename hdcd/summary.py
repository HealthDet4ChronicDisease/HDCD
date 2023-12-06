"""
Summary module
"""

### --- TODO ----###
### Add __all__ to the import * in __init__
### Add use_case demonstration functions as a helper
### Add more statement if/else to specify if variables are not encountered and
### notify the user to change the data format

__all__ = ['data_summary',"variable_summary"]

def data_summary(dataframe):

    """
    print out summary of data
    """

    n_cols = len(dataframe.columns)
    n_rows = len(dataframe)
    print(f'The dataframe contains {n_cols} of columns and {n_rows} of rows \n')

    n_topics = dataframe["Topic"].nunique()
    n_questions = dataframe["Question"].nunique()

    print(f'The dataframe contains {n_topics} topics and {n_questions} \
questions \n')

    topics = dataframe["Topic"].unique()
    print(f'The list of topics including {list(topics)} \n')

    stratifications = dataframe["StratificationCategory1"].unique()
    print(f'The stratifications of the variables including \
{list(stratifications)} \n')

    print('The set of functions and tools are designed to analyze the chronic \
disease index (dataframe) data from the CDC. For more information, print out the \
[Question] variables from the dataset and explore them under the [Topic] \
variable')


def variable_summary(variable, dataframe):

    """
    give description of the variable, including:
    variable unit in [DataValueType] column,
    variable prevalence longitudinally in [YearStart] column,
    variable prevalence across different state in [LocationAbbr] column
    """

    dataframe = dataframe[dataframe["Question"] == variable]

    units = dataframe["DataValueType"].unique()
    print(f'variable units including {units}')

    n_states = dataframe.dropna(subset = ["DataValue"])["LocationAbbr"].nunique()
    n_states_total = dataframe["LocationAbbr"].nunique()
    print(f'numbers of geo-location (states) have data available: \
{n_states}/{n_states_total}')

    n_year = dataframe.dropna(subset = ["DataValue"])["YearStart"].unique()
    print(f'numbers of unique years have data available: {len(n_year)}, \
from {min(n_year)} to {max(n_year)}')
