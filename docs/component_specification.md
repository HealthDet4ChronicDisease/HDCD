# Component Specification

## Software Components
* Describe at least 3 components specifying: what it does, inputs 
it requires, and outputs it provides

**1. GeoMap**
* *What it does:* Displays geographic boundaries for US states and
 counties on a projection
* *Inputs:* Geographic shape data (states and counties) for the
 contiguous US, Alaska, and Hawaii
* *Outputs:* Albers projection of US states and counties on a 
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
 area and SDOH, they could select  one SDOH to display. The selected SDOH 
 would appear on the *GeoMap* as a colored choropleth.

## Preliminary Plan
*  A list of tasks in priority order.