# Health Determinants for Chronic Diseases
This project is in fulfillment of the final delieverable for the Fall 2023 CSE 583 course at University of Washington.

**Team**: Brian Chang, Peter Ju, Wesley Surento, Su Xian

## Background
Social determinants of health (SDOH) are "societal systems, their components, and the social resources and hazards for health that societal systems control and distribute, allocate and withhold, such that the demographic distribution or trend of health outcomes is changed." [[1]](#1) These societal systems include governments, institutions, and other organizations, which "control and distribute, allocate and withhold" resources and hazards for health, such as food, income, employment, education, and health information.

SDOH have become an increasingly growing area of research within the health community. A compelling body of work has shown that social factors play important roles in health outcomes. For example, multiple studies have demonstrated a stepwise gradient pattern in the association between income and health - health improves incrementally as income rises. However, the association between SDOH and health outcomes can be complicated, as there are many complex biopsychosocial and biophysiosocial pathways and processes. [[2]](#2)

To explore and analyze such complex relationships, interactive visualizations can aid researchers and public health experts in "knowledge discovery, hypotheses generation, and decision support." [[3]](#3)[[4]](#4) Interactive visuzliations can play an important role in fostering knowledge generation and help in establishing associations and causality, as they allow for direct data manipulation and analysis.

## Objective
Our goal for this project is to deploy interactive visualizations with a focus on SDOH, which can vary in their distribution across space and time, and their associations with chronic diseases, such as cardiovascular disease. Specifically, we would like to make this process as easy as possible so that a user with minimal technical experience can utilize the interactive visualizations. From interacting with said visualizations, the question we would like to help users answer is: *"Can we identify emerging trends and establish associatons between SDOH and health outcomes?"*

## Dataset
For demonstration purposes, we collected data from different sources, including publicly available Centers for Disease Control and Prevention (CDC) datasets, [Chronic Disease Index (CDI)](https://chronicdata.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators-CDI-/g4ie-h725/data) and [500 PLACES](https://www.cdc.gov/places/about/500-cities-2016-2019/index.html), and also protected data from the *All of Us Research Program*.

As we envision an interactive visualization tool to be widely applicable, we opted to use the [*All of Us Research Program*](https://allofus.nih.gov/), an effort by the National Institues of Health (NIH) that consists of a diverse group of at least one million participants across the United States. [[5]](#5) This data consortium includes health questionnaires, electronic health records, digital health technology data, and biospecimens. Importantly, it includes key SDOH, such as income, education, and housing status. The dataset also uses the [Observational Medical Outcomes Partnership Common Data Model](https://www.ohdsi.org/data-standardization/) to standardize all data. As multiple data repositories currently use *OMOP*, our project will be applicable to these as well and scalable.

Researchers can gain access to the *All of Us Research Program* through the [All of Us Research Hub](https://www.researchallofus.org/). Some limitations of this dataset is that it requires extensive training to gain approval for the controlled-tier dataset, which includes participant-level data. Also, any analysis and visualization must be performed within the *All of Us Research Hub* workbench. Participant-level data cannot be exported locally.

## Organization of the Project
``````
HDCD/
┣ .github/
┃ ┗ workflows/
┃   ┗ python-package-conda.yml
┣ data/
┃ ┣ cdi_dummy.csv
┃ ┣ conditions.csv
┃ ┣ conditions.xlsx
┃ ┣ condition_data.csv
┃ ┣ observation_data.csv
┃ ┣ person_data.csv
┃ ┣ places_dummy.csv
┃ ┗ survey_data.csv
┣ docs/
┃ ┣ 2023-11-14.pptx
┃ ┣ component_specification.md
┃ ┣ design.md
┃ ┣ functional_specification.md
┃ ┗ HDCD_Presentation_slides.pptx
┣ examples/
┃ ┣ Depression_condition_visual_example.html
┃ ┣ education.html
┃ ┣ health_insurance.html
┃ ┣ Lets Get Started....html
┃ ┣ median_income.html
┃ ┗ poverty.html
┣ hdcd/
┃ ┣ data_wrangling.py
┃ ┣ plot.py
┃ ┣ summary.py
┃ ┗ __init__.py
┣ notebook/
┃ ┣ dummy_data.ipynb
┃ ┣ Lets Get Started....ipynb
┃ ┗ test_geomap.ipynb
┣ tests/
┃ ┗ test.py
┣ .gitignore
┣ config.py
┣ environment.yml
┣ LICENSE
┣ main.py
┗ README.md
``````

## Quick Start -- Example using Jupyter notebook with Chronic Disease Index (CDI) Data
A step-by-step illustration of HDCD tool use is available [here](https://htmlpreview.github.io/?https://github.com/HealthDet4ChronicDisease/HDCD/blob/main/examples/Lets%20Get%20Started....html).

## Setup and Installation
* *Note:* Some modules will only produce visualizations within the *All of Us Research Workbench* with queried data. These are marked by **AoU** below. When working locally, please refer to the dummy data in `data`, which has been set in `config.py`. We recommend starting with summary statistics for the CDI data, as shown in the notebook.

1. Clone this GitHub repository to your local working directory with
the command:
``````
git clone https://github.com/HealthDet4ChronicDisease/HDCD.git
``````
2. Create a local conda environment with the necessary Python packages
``````
conda create --name <ENV_NAME> -f environment.yml
conda activate <ENV_NAME>
``````
3. Adjust the parameters in `config.py` for the variables and stratification you want to visualize. These are passed to `main.py` upon running step 4.
<br/>

4. Run modules
* *plot_longitudinal* (default = False): if called, set to 'True'
    * output: longitudinal time-series graph of variables in `config.py`
* *plot_correlation* (default = False): if called, set to 'True'
    * output: scatterplot of two SDOH and outcome in `config.py`
* *plot_geomap*: select type from ['socioeconomic', 'conditions', 'geomap']
    * socioeconomic **(AoU)**: income, education, health insurance, and poverty geomaps
    * conditions **(AoU)**: geomap of queried conditions data
    * geomap: CDI data geomap of variables in `config.py`
* *summary_statistics*: select type from ['data', 'variable']
    * output: prints number and type of data or variables for a dataset in `config.py`
``````
python main.py \
    [--plot_longitudinal] # longitudinal time series graph of two variables \
    [--plot_correlation] # scatterplot of two variables \
    [--plot_geomap] # interactive geomap of selected type \
    [--summary_statistics] # prints summary of dataset or variable
``````

5. **Note:** The following module will not run locally:
``````
python main.py --plot_geomap=socioeconomic
``````
as the county-level socioeconomic data requires data directly from *All of Us*.

The following module:
``````
python main.py --plot_geomap=conditions
``````
will run locally for testing as there are dummy csv files in `data`.

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
