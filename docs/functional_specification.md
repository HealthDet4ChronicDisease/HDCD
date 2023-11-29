# Functional Specification

## Background
Social determinants of health (SDOH) have become an increasingly growing area of research for the health community. A compelling body of work has shown that social factors play important roles in health outcomes. Multiple studies have demonstrated a stepwise gradient pattern in the association between income and health - health improves incrementally as income rises. However, the association between SDOH and health outcomes can be complicated, as there are many complex biopsychosocial and biophysiosocial pathways and processes.

To explore and analyze such complex relationships, interactive visualizations can aid researchers and public health experts in "knowledge discovery, hypotheses generation, and decision support." [[1]](#1)[[2]](#2) Interactively visuzliations can play an important role in fostering knowledge generation and help in establishing associations and causality, as they allow for direct data manipulation and analysis. However, creating interactive visualizations can be a technically intensive and arduous task, requiring both technical and data visualization experience. We would like to make this process as easy as possible so that a user with minimal technical experience can create and utilize the interactive visualizations.

## User Profile
1. The user is a public health official who is interested in public health data and wants to gain hands-on experience working with public datasets. They want to use the tool for  basic visualizations,  summary statistics, and/or simple association studies. They can use the inferences made based on the tool to support their policy proposal, as well as bring attention to new health issues and trends. Their skill set should comprise of domain knowledge about public health.

2. The user is a data scientist who specializes in public health. They want to perform analysis on public datasets to support their own research and explore mechanism that link SDOH and health outcomes. They have strong technical skills in a few programming languages and should be able to perform data analysis.

3. The user is a medical doctor interested in exploratory analysis of SDOH to identify trends and associated health outcomes longitudinally to form hypotheses for a grant application. The doctor would be using these data as supportive materials for said grant application.

## Data Sources
As we envision an interactive visualization tool to be widely applicable, we opted to use the *All of Us Research Program*, an effort by the National Institues of Health (NIH) that consists of a diverse group of at least one million participants across the United States. [[3]](#3) This data consortium includes health questionnaires, electronic health records, digital health technology data, and biospecimens. Importantly, it also includes key SDOH, such as income, education, and housing status.

Researchers can gain access to the *All of Us Research Program* through the [All of Us Research Hub](https://www.researchallofus.org/). Some limitations of this dataset is that it requires training to gain approval for the controlled-tier dataset, which includes participant-level location data. Also, any analysis and visualization must be performed within the *All of Us Research Hub* workbench. Data cannot be exported locally.

## Use Cases
**1. What is the distribution of homelessness within the greater Seattle area and is there an association to mental health disorders?**
- The objective of this user interaction is to have the user create and interact with a geomap, consisting of interactive legends for housing status and various mental health disorders (e.g., major depressive disorder).
- We expect the user to pan and zoom the geomap, hide and show different levels of housing status with the interactive legends, and draw conclusions based on the various levels of data they choose to hide and show.

**2. Is there a trend in obesity stratified by income and county within the greater Seattle area?**
- The objective of this user interaction is to have the user create and interact with time series graphs with interactive legends for income and/or a geomap, consisting of a sliding scale for time (in years).
- We expect the user to hide and show different levels of income on the time-series graphs and interact with the sliding scale on the geomap to draw conclusions based on the various levels of data they choose to hide and show. They may choose to show the time-series graphs and geomap side-by-side.

<a id="1">[1]</a>
*Chishtie J, Bielska IA, Barrera A, et al.* **Interactive Visualization Applications in Population Health and Health Services Research: Systematic Scoping Review.** J Med Internet Res. 2022;24(2):e27534. Published 2022 Feb 18.
[![DOI:10.2196/27534](https://zenodo.org/badge/DOI/10.2196/27534.svg)](https://doi:10.2196/27534)

<a id="2">[2]</a>
*Zakkar M, Sedig K.* **Interactive visualization of public health indicators to support policymaking: An exploratory study.** Online J Public Health Inform. 2017;9(2):e190. Published 2017 Sep 8.
[![DOI:10.5210/ojphi.v9i2.8000](https://zenodo.org/badge/DOI/10.5210/ojphi.v9i2.8000.svg)](https://doi:10.5210/ojphi.v9i2.8000)

<a id="3">[3]</a>
*The “All of Us” Research Program.* New England Journal of Medicine. 2019;381(7):668-676. doi:10.1056/NEJMsr1809937
[![DOI:10.1056/NEJMsr1809937](https://zenodo.org/badge/DOI/10.1056/NEJMsr1809937.svg)](https://doi:10.1056/NEJMsr1809937)