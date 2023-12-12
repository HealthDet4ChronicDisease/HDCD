# Component Specification

## Software Components
**1. GeoMap**
* *What it does:* Displays geographic boundaries for US states and
 counties on a projection
* *Inputs:* Geographic shape data (states and counties) for the
 contiguous US, Alaska, and Hawaii
* *Outputs:* Albers USA projection of US states and counties on a 
projection of size to be determined by the user

**2. Social determinants of health (SDOH) selector**
* *What it does:* Allows a user to interactively select various SDOH
 to visualize
* *Inputs:* SDOH - income level, healthcare coverage, occupation status,
 and housing status from dataset 
* *Outputs:* An interactive legend or drop-down menu to select which
 SDOH to display on the visualization

 **3. Sliding Scale for Time**
* *What it does:* Allows a user to interactively select a time point
* *Inputs:* datetime stamps for SDOH observations 
* *Outputs:* An interactive sliding scale that allows the user to click
and drag to specific time points to display

## Interactions for Use Cases
The *GeoMap* and *SDOH selector* interact so that a user can select
 which SDOH to visualize on a map projection for aggregate participant 
 data. For example, if a user wanted to look for associations between 
 rates of  cardiovascular disease (CVD) by county within the great Seattle 
 area and SDOH, they could select one SDOH to display. The selected SDOH 
 would appear on the *GeoMap* as a colored choropleth.

## Preliminary Plan
1. Get access to *All of Us* dataset.
2. Decide on interactive visualizations and determine what 
    data points are necessary.
3. Perform exploratory analysis and summary statistics of SDOH 
    data in *All of Us*.
4. Wrangle and clean *All of Us* datasets for interactive visualizations.
5. Produce interactive visualizations and iteratively update depending on
    usability of interactions.
6. Compile interactive visualizations to functions and classes as needed.
7. Declare unit tests for each visualization type.