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

**2. Something Else Here**

**3. Social determinants of health (SDOH) selector**
* *What it does:* Allows a user to interactively select various SDOH
 to visualize
* *Inputs:* SDOH - income level, healthcare coverage, occupation status,
 and housing status from dataset 
* *Outputs:* An interactive legend or drop-down menu to select which
 SDOH to display on the visualization

## Interactions for Use Cases
The *GeoMap* and *SDOH selector* interact so that a user can select
 which SDOH to visualize on a map projection for aggregate participant data. For
 example, if a user wanted to look at rates of cardiovascular disease (CVD) by county 
 within the great Seattle area, they could select between income and healthcare 
 coverage to see if there is an association between either SDOH and CVD rates. 
 The selected SDOH would appear on the *GeoMap* as a colored choropleth.

## Preliminary Plan
*  A list of tasks in priority order.