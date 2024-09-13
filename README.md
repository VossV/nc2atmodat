# nc2atmodat                                                  
Processing scripts for obstacle resolving model (ORM) datasets


How to process datasets:
====================================

1) Download this code from gitlab with:

> git clone git@gitlab.dkrz.de:memi/nc2atmodat.git

2) Go to directory process_model_data

> cd process_model_data

You find here the following files:
- process_model_data.py   (main programm)
- dict_OUTPUT_variables.py   (pre-selected output variables)
- dict_custom_variables_attributes.py (additional variable information)
- Metadata_for_atmodat_standard.xlsx (metadata information)

3) open "Metadata_for_atmodat_standard" with Microsoft Excel and modify the sheet 

4) open "process_model_data.py" with an text editor:

5) set 'path', 'file', 'Metadata_file' in the user input section.

6) set switches: 
- if you use your own reference point 
- or if you want to crop your data to an certain extend. 

7) If you want to write specific variables add them to 'custom_variables' or add variables to "dict_OUTPUT_variables.py".

8) Run script with python

> module load python3
> ipython process_model_data.py

or

> ipython process_model_data.ipynb

or

> python process_model_data.py


to translate process_model_data.ipynb to an python file:
>  "jupyter nbconvert --to script process_model_data.ipynb"


Required Python Modules:
------------------------

- xarray
- netCDF4 
- numpy 
- pyproj 
- pandas
- dask


Description of files:
===============================

Directory process_model_data:
-----------------------------
If you want to standardise your data go to process_model_data
This directory contain the following files:

- process_model_data.py      (Main script to run the code)
- dict_OUTPUT_variables.py   (Pre-Selected output)
- dict_cutsom_variables.py   (Additional variable information)
- functions.py               (Functions to run the code)
- Metadata_for_atmodat_standard.xlsx  (Metadata Information)


process_model_data.py
---------------------
- main program
- add here path, input-file, output-file and metadata-file
- rewrite coordinates and dimensions
- add georeferencing to dataset by adding geographical and utm coordinates
- removes variables that are not meant for publication.


functions.py
------------
- contains all functions used for process_model_data.py

dict_OUTPUT_variables.py 
---------------------------
- contains dictionaries with all variables that should be published

dict_custom_variables_attributes.py 
---------------------------
- contains dictionaries with variables and attributes.
- user specific descriptions for variables can be added here.
  e.g. tracer = pm10, pm2.5 or comments on the variables (references, explanations)


Metadata_for_atmodat_standard.xlsx
----------------------------------
- contains global metadata that should be added to the file.
- must be filled by the producer for each dataset individually
 


