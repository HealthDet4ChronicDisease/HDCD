# User stories
- The user is a policy maker who is interested in public health data and wants to have some hands-on experiences working with public dataset. They want to use the tool for some basic visualizations, and summary statistics, or some simple association studies. They can use the inferences made based on the tool to support their policy proposal or bring new health issues/trends. Their skill levels should at least contain basic python knowledge, and domain knowledge about health issues/problems.

- The user is a data scientist who specializes in public health. He wants to perform some analysis on the public data to support his own research and explore some mechanism that links behavior and public health. He is skilled in a few programming languages and should be able to perform individual analysis.

- A medical doctor interested in identifying health trends and related behavior issues longitudinally to start some observations or forming hypotheses for a grant application. The doctor would be using these data as some supportive materials

# Functional design (TO EDIT)

- Data visualization for pattern recognition
- Preliminary results for grant application
- Predictive modeling

### Example
The individual in question displays a keen interest in the domain of public health data and seeks to gain practical exposure to the manipulation of publicly available datasets. This engagement with data entails a desire to employ the tool for fundamental data visualizations, generation of summary statistics, or the conduct of rudimentary association studies. The outcomes derived from this tool-driven analysis may serve as substantiation for policy recommendations or the identification of emerging health-related concerns and trends. A prerequisite for the user is a foundational proficiency in the Python programming language and a solid understanding of the domain-specific intricacies related to health issues and problems.

# Component Example

- Name : SummaryStatistics
- What it does: It describes the general distribution given an outcome variable. Automatically generate a report for missingness, plot for trending of year and differences by state.
- Inputs: Health outcome fields from dataset
- Outputs: Output a text report for missingness, a plot for variable distribution by year (longitudinal) and by state (geographical)
How use other components:

# Use case (TODO)
