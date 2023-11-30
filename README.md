# Health Data Analysis for Chronic Diseases
This project is in fulfillment of the final delieverable for the CSE 583 course at University of Washington.

## Background
Social determinants of health (SDOH) are "societal systems, their components, and the social resources and hazards for health that societal systems control and distribute, allocate and withhold, such that the demographic distribution or trend of health outcomes is changed." [[1]](#1) These societal systems include governments, institutions, and other organizations, which "control and distribute, allocate and withhold" resources and hazards for health, such as food, income, employment, education, and health information.

SDOH have become an increasingly growing area of research within the health community. A compelling body of work has shown that social factors play important roles in health outcomes. For example, multiple studies have demonstrated a stepwise gradient pattern in the association between income and health - health improves incrementally as income rises. However, the association between SDOH and health outcomes can be complicated, as there are many complex biopsychosocial and biophysiosocial pathways and processes. [[2]](#2)

To explore and analyze such complex relationships, interactive visualizations can aid researchers and public health experts in "knowledge discovery, hypotheses generation, and decision support." [[3]](#3)[[4]](#4) Interactive visuzliations can play an important role in fostering knowledge generation and help in establishing associations and causality, as they allow for direct data manipulation and analysis.

## Objective
Our goal for this project is to deploy interactive visualizations with a focus on SDOH, which can vary in their distribution across space and time, and their associations with chronic diseases, such as cardiovascular disease. Specifically, we would like to make this process as easy as possible so that a user with minimal technical experience can utilize the interactive visualizations. From interacting with said visualizations, the question we would like to help users answer is: *"Can we identify emerging trends and establish associatons between SDOH and health outcomes?"*

## Dataset
As we envision an interactive visualization tool to be widely applicable, we opted to use the [*All of Us Research Program*](https://allofus.nih.gov/), an effort by the National Institues of Health (NIH) that consists of a diverse group of at least one million participants across the United States. [[5]](#5) This data consortium includes health questionnaires, electronic health records, digital health technology data, and biospecimens. Importantly, it includes key SDOH, such as income, education, and housing status. The dataset also uses the [Observational Medical Outcomes Partnership Common Data Model](https://www.ohdsi.org/data-standardization/) to standardize all data.

Researchers can gain access to the *All of Us Research Program* through the [All of Us Research Hub](https://www.researchallofus.org/). Some limitations of this dataset is that it requires extensive training to gain approval for the controlled-tier dataset, which includes participant-level data. Also, any analysis and visualization must be performed within the *All of Us Research Hub* workbench. Data cannot be exported locally.

# References
<a id="1">[1]</a>
*Hahn RA.* **What is a social determinant of health? Back to basics.** J Public Health Res. 2021;10(4):2324. Published 2021 Jun 23.
[![DOI:10.4081/jphr.2021.2324](https://zenodo.org/badge/DOI/10.4081/jphr.2021.2324.svg)](https://doi.org/10.4081/jphr.2021.2324)

<a id="2">[2]</a>
*Braveman P, Gottlieb L.* **The social determinants of health: it's time to consider the causes of the causes.** Public Health Rep. 2014;129 Suppl 2(Suppl 2):19-31.
[![DOI:10.1177/00333549141291S206](https://zenodo.org/badge/DOI/10.1177/00333549141291S206.svg)](https://doi.org/10.1177/00333549141291S206)

<a id="3">[3]</a>
*Chishtie J, Bielska IA, Barrera A, et al.* **Interactive Visualization Applications in Population Health and Health Services Research: Systematic Scoping Review.** J Med Internet Res. 2022;24(2):e27534. Published 2022 Feb 18.
[![DOI:10.2196/27534](https://zenodo.org/badge/DOI/10.2196/27534.svg)](https://doi.org/10.2196/27534)

<a id="4">[4]</a>
*Zakkar M, Sedig K.* **Interactive visualization of public health indicators to support policymaking: An exploratory study.** Online J Public Health Inform. 2017;9(2):e190. Published 2017 Sep 8.
[![DOI:10.5210/ojphi.v9i2.8000](https://zenodo.org/badge/DOI/10.5210/ojphi.v9i2.8000.svg)](https://doi.org/10.5210/ojphi.v9i2.8000)

<a id="5">[5]</a>
*The “All of Us” Research Program.* New England Journal of Medicine. 2019;381(7):668-676. Published 2019 Aug 5.
[![DOI:10.1056/NEJMsr1809937](https://zenodo.org/badge/DOI/10.1056/NEJMsr1809937.svg)](https://doi.org/10.1056/NEJMsr1809937)
