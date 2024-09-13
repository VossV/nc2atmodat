#!/usr/bin/env python
# coding: utf-8

# Author: Vivien Voss (u300648)
# Contributors: Daniel Heydebreck (DKRZ), Angelika Heil (DKRZ)
###############################################################################
#               nc2atmodat/process_model_data.py  
###############################################################################
#
#=============================================================================#
# User Input 
#-----------------------------------------------------------------------------#
path     = '/path/to/files/'
files   =  ['file1.nc', "file2.nc", "file3.nc"]
metadata = 'Metadata_for_atmodat_standard.xlsx'


# Custom settings
#-----------------------------------------------------------------------------#
# 1) Set custom reference point coordinates (UTM)
#    True/False, default: False
use_own_REF = True 
#                                                      
# Custom coordinates in UTM
XREF = 565946.0009999999
YREF = 5933915.5540000005

#-----------------------------------------------------------------------------#
# 2) crop domain size:  
#    True/False, default: False
# INFO: soll i < iv, aufpassen mit der wahl der indicies.
use_own_ijk = False
ii = [9,730]
jj = [12,773]
kk = [0,50]
#-----------------------------------------------------------------------------#
# 3) add additional variables to output (name)
#    comma separated list: ['var1', 'var2', ...]
custom_variables = [] #['tket']
#
#-----------------------------------------------------------------------------#
# END User Input 
#=============================================================================#

# load modules
import xarray as xr
import numpy as np
from pyproj import Proj, CRS
import pandas as pd
from datetime import datetime
from dask.diagnostics import ProgressBar
#-----------------------------------------------------------------------------#
# load custom modules
from dict_MEMI_record_numbers import *
from functions import *
#-----------------------------------------------------------------------------#


for infile in files:
    outfile  = 'nc2atmodat_'+infile


    # Read netCDF-File
    #-------------------------------------------------------------------------#
    data = READ_FILE(path + infile)


    # crop data by size
    #-------------------------------------------------------------------------#
    ncid = CROP_DATA(data, use_own_ijk, ii, jj, kk)


    # Create dimensions i,j,k
    #-------------------------------------------------------------------------#
    ncid = REASSIGN_DIMENSIONS(ncid)
    ncid = CREATE_BOUNDS(ncid)

    # OPTIONAL: Create time bounds (TODO)
    #-------------------------------------------------------------------------#
    ncid = ADD_TIME_ATTRS(ncid)


    # Add UTM and geographic coordinate
    #-------------------------------------------------------------------------#
    # Projection: universal transversal mercator
    projection = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=False)
    ncid       = GEOCOORDINATES(ncid, projection, use_own_REF, XREF, YREF)
    #ncid       = GEOCOORDINATES_VECTOR(ncid, projection, use_own_REF, XREF, YREF)  # optional
    ncid       = SET_ijk_TO_xyz(ncid)
    ncid       = CELL_METHODS(ncid)
    #ncid       = ADD_CELL_METHODS(ncid)    # optional


    # Select Output Variables
    #-------------------------------------------------------------------------#
    ncoutput = SELECT_OUTPUT_VARIABLES(ncid, custom_variables)
    ncoutput = ADD_CUSTOM_ATTRIBUTES_TO_VARIABLES(ncoutput)
    ncoutput = CORRECTION_VARIABLE_ATTRIBUTES(ncoutput)


    # Global Attributes
    #-------------------------------------------------------------------------#
    ncoutput.attrs            = ADD_GLOBAL_ATTRS(metadata)
    ncoutput.attrs['history'] = ADD_GLOBAL_HISTORY_ATTRS(path + infile)
    ncoutput                  = DELETE_GLOBAL_ATTRS(ncoutput)

    # OPTIONAL: Grid Mapping and Projection (TODO)
    #-------------------------------------------------------------------------#
    #! INFO: only required if lat, lon are not in the dataset.
    #! See more info at the function.
    # XARR = GRID_MAPPING(XARR, PROJECTION) <---- WIP


    #==============================================================================
    # save file, end processing:
    #-------------------------------------------------------------------------#
    # dividing file into chunks ( useful for limited memory)
    #rechunked = ncoutput.chunk({'i': 400, 'j': 400}) #    3 min
    rechunked = ncoutput.chunk({'x': 400, 'y': 400}) #    3 min
    write_job = rechunked.to_netcdf(path + outfile, compute=False, engine='netcdf4')
    with ProgressBar():
        print(f" INFO: Writing to {outfile}")
        write_job.compute()
    ncid.close()
    ncoutput.close()
    #-------------------------------------------------------------------------#
    print('Finished \n file can be found here:\n ' + path + outfile)


###############################################################################
#               nc2atmodat/process_model_data.py  
###############################################################################
#EOF
