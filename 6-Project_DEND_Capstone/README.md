<h1>US Immigration</h1>
<h3>Data Engineering Capstone Project</h3>

<h3>Project Summary</h3>
The goal of this project was to develop an ETL pipeline in order search immigration data related to temperature and city demographics. In constructing the pipeline, I focused on addressing 3 primary questions in order to perform data cleaning and mapping the pipeline:
<ol> 
    <li>Which cities do immigrants tend to move and where did they come from?</li>
<li>Does temperature play a role on where people on temporary visas go?</li>
    <li>Did the demographic counted in the US_Cities-Demographics dataset correspond at all where immigrants tend to travel?</li>
</ol>

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

<h3>Data Sets</h3>
The data sets used for this project are:
<ul>
    <li>Immigration Data</li>
    <li>US Cities Demographics</li>
    <li>Earth Surface Temperature Data</li>
</ul>

<h4>Immigration Data</h4>
The data comes from the US National Tourism and Trade Office and provided by Udacity. A data dictionary is provided within the file I94_SAS_Labels_Descriptions.SAS. I added Visa code descriptions to the data dictionary as I plan to use the visa types in my project.
The data set was taken from <a href="https://travel.trade.gov/research/reports/i94/historical/2016.html">this link</a>.
The dataset can be previewed from the immigration_data_sample.csv file. The full dataset consists of several SAS files which are located within the
SAS_data folder.  

<h4>US Cities Demographics</h4>
The data comes from <a href="https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/">OpenSoft</a>. The dataset contains information about the demographics of all US cities and census-designated places with a population greater or equal to 65,000. This data comes from the US Census Bureau's 2015 American Community Survey <a href="https://www.census.gov/data/developers/about/terms-of-service.html">and is referenced in this link. </a> 

<h4>World Temperature Data</h4>
The dataset is provided by <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons BY-NC-SA 4.0 </a>.  


<h3>Data Model</h3>
I chose to use a star schema with the immigration dataset combined with temperature data chosen to be the fact table and the temperature,  city demographics, and immigration datasets chosen to be dimension tables.
