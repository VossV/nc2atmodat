#!/usr/bin/env python
# coding: utf-8

#-- Load Modules
#-------------------------------#
import xarray as xr
#from netCDF4 import Dataset
import numpy as np
from pyproj import Proj, CRS
import pandas as pd
from datetime import datetime
import os
from dask.diagnostics import ProgressBar

#=============================================================
def READ_FILE(FILE):
    """
    read netCDF with xarray. 
    INPUT: FILE = filename or path and file
    OUTPUT: data = xarray of FILE
    using xarray module
    """
    
    #--- try to open file, if file not found, raises error
    try:
        XARR = xr.open_dataset(FILE, engine='netcdf4', drop_variables=('nsfccl'))
        print('INFO: netCDF open')
        CHECK_REQUIRED_VARIABLES(XARR)
    except FileNotFoundError:
        print('ERROR: NetCDF file not found. Stopping program.')
        raise SystemExit(1)
    
    return XARR

#=============================================================

def CHECK_REQUIRED_VARIABLES(XARR):
    required_var = ['xsmet', 'ysmet', 'zsmet', 'xvmet', 'yvmet', 'zvmet', 'elam', 'ephi', 'lon', 'lat']    
    try: 
        for var in required_var:
            if var in list(XARR.variables):
                pass
    except:
        print('INFO: some required variables are not in the Dataset, check your data for: ', end=' ')
        print(required_var)
        pass
        #raise SystemExit(1)
        
        
#=============================================================

def CROP_DATA(DATA, SWITCH, II,JJ,KK):
    """
    User Input: Crop your data to a specific size.
    This is necessary to create bounds for the grid cells
    required dimensions: i,j,k
    optional dimensions: iv, jv, kv
    dimensions must be iv < i; iv = i + 1, similar for j and k
    INPUT: DATA = inital xarray file 
    OUTPUT: XARR = Cropped xarray file
    using xarray module
    """
    
    if SWITCH == True:
        try:
            if 'iv' and 'jv' and 'kv' in list(XARR.dims):
                XARR = DATA.isel(i=slice(II[0]+1,II[1]-1), iv=slice(II[0], II[1]-1),
                                 j=slice(JJ[0]+1,JJ[1]-1), jv=slice(JJ[0], JJ[1]-1),
                                 k=slice(KK[0]+1,KK[1]-1), kv=slice(KK[0], KK[1]-1))
                print('INFO: crop file to size i={},{}, j={},{}, k={},{}'.format(II[0],II[1], JJ[0],JJ[1], KK[0],KK[1]))
        except ValueError:
            print('ERROR: crop file: insert valid range for i,j,k. stopping programm')
            raise SystemExit(1)
    else:
        try:
            XARR = DATA.isel(i=slice(1,-2), j=slice(1,-2),k=slice(1,-2),
                         iv=slice(0,-1), jv=slice(0,-1),kv=slice(0,-1))
        except:
            XARR = DATA.isel(i=slice(1,-2), j=slice(1,-2),k=slice(1,-2))
            
    DATA.close()
    return XARR        

def CROP_TIME(DATA, SWITCH, TT):
    """
    USER INPUT: Crop data to a specific time frame
    """

    if SWITCH == True:
        try:
            XARR = DATA.isel(time=slice(TT[0],TT[1]))
            print('INFO: crop file to timesteps={},{}'.format(TT[0],TT[1]))
        except ValueError:
            print('ERROR: crop file: insert valid range for time. Stopping programm')
            raise SystemExit(1)

    else:
        print('INFO: timesteps not reduced')
    DATA.close()
    return XARR  


#=============================================================
def REASSIGN_VERTICAL_DIMENSIONS(XARR):
    """
    if orography exists in the model domain, k is different for each cell.
    therefore we need level instead of z coordinate.
    """
    try:
        zsurf = XARR.yzsurf

        #CASE: no orography:
        if zsurf.values.mean() == 0:        
            # create k as variable
            kval = np.empty((XARR.k.size), 'f8')

            # get values for k from zsmet:   
            for i in range(len(kval)):
                kval[i] = XARR.zsmet[i+1].values.copy()  
            kval[-1] = kval[-2] + (kval[-2] - kval[-3])

            # assign as new variables to data
            XARR['k'] = (['k'], kval)

            # definition of attributes for new variable k
            k_attr = {'long_name' : 'k_position',
                      'standard_name' : 'height',
                      'axis' : 'Z',
                      'positive': 'up',
                      'units' : 'm',
                      'bounds' : 'k_bnds'}

            # add attributes to k
            XARR.k.attrs = k_attr 
            print('INFO: adding k (1D) to ncfile')     

        #CASE: orography! # k = 3D
        elif zsurf.values.mean() != 0:   

            # create lev as variable
            kval = np.empty((XARR.k.size), 'i4')

            # get values for level:   
            for i in range(len(kval)):
                kval[i] = i  

            # assign as new variables to data
            XARR['k'] = (['k'], kval)

            # definition of attributes for new variable k
            kval_attr = {'long_name' : 'model level',
                         'axis' : 'Z',
                         'positive': 'up'}

            # add attributes to k
            XARR.k.attrs = kval_attr
            print('INFO: adding k (3D) to ncfile') 
        
        
            # Add 3D zsmet
            XARR = XARR.drop_vars("zsmet")
            zsmet_3D = np.ndarray((XARR.k.size,XARR.j.size, XARR.i.size))
            #
            zsmet_3D = XARR.zvmet[0:-1] + 0.5*( XARR.zvmet[1::] - XARR.zvmet[0:-1])
            #
            XARR['zsmet'] = (['k', 'j', 'i'], zsmet_3D.data)         
            zsmet_attr = {'long_name' : 'vertical_distance_above_ground',
                          'standard_name' : 'height',
                          'units' : 'm'}
            XARR['zsmet'].attrs = zsmet_attr
            print('INFO: adding zsmet (3D) to ncfile')
                          

        else:
            print('INFO: k coordinate is not properly assigned')
            pass
    except:
        print('---> yzsurf not in dataset')

    return XARR



def SET_ijk_TO_xyz(XARR):
    """
    WIP: Preparation on how to rename dimensions and coordinates
         from ijk to xyz.. if requested
    """
    if 'i' and 'j' in list(XARR.dims):
        
        replace_dims = {'i':'x', 'j':'y'}
        XARR = XARR.rename_dims(dims_dict=replace_dims)
        XARR = XARR.rename_vars(name_dict=replace_dims)
          
        x_attr = {'long_name' : 'x_position',
                  'axis' : 'X',
                  'units' : 'm'
                 }
        
        y_attr = {'long_name' : 'y_position',
              'axis' : 'Y',
              'units' : 'm'
                 }
        
        XARR.x.attrs = x_attr 
        XARR.y.attrs = y_attr 
        print('INFO: SET_ijk_TO_xyz: i, j renamed to x,y')

        # Add bounds to i,j, if applicable
        if 'i_bnds' and 'j_bnds' in list(XARR.coords):
            replace_coord = {'i_bnds' : 'x_bnds', 'j_bnds' : 'y_bnds'}
            XARR = XARR.rename(replace_coord)
            ncid['x'].attrs['bounds'] = 'x_bnds'
            ncid['y'].attrs['bounds'] = 'y_bnds'
            print('INFO: SET_ijk_TO_xyz: x_bnds, y_bnds added')
        else:
            print('INFO: SET_ijk_TO_xyz: i_bnds, j_bnds not assigned.')
                        

        if 'iv' and 'jv' in list(XARR.dims):
            replace_dims = {'iv' :'xv', 'jv':'yv'}
            XARR = XARR.rename_dims(dims_dict=replace_dims)
            XARR = XARR.rename_vars(name_dict=replace_dims)
            print('INFO: SET_ijk_TO_xyz: iv, jv renamed to xv, yv')          
           

    try: 
        # MITAS variable for orography height 
        if XARR.yzsurf.values.mean() == 0:
            print('INFO: k will be renamed to z')
            replace_dims = {'k':'z'}
            XARR = XARR.rename_dims(dims_dict=replace_dims)
            XARR = XARR.rename_vars(name_dict=replace_dims)
            
            replace_coords = {'k_bnds' : 'z_bnds'}
            XARR = XARR.rename(replace_coords)
            
            z_attr = {'long_name' : 'z_position',
              'standard_name' : 'height',
              'axis' : 'Z',
              'positive': 'up',
              'units' : 'm',
              'bounds' : 'z_bnds'}
            XARR.z.attrs = z_attr
            
        elif XARR.yzsurf.values.mean() != 0:
            pass
        
        else:
            print('INFO: no vertical cooridnate')
    except:
        pass
        
            
    print('INFO: SET_ijk_TO_xyz: ijk are renamed to xyz')
    return XARR



def REASSIGN_DIMENSIONS(XARR):
    """
    i,j,k are used as index.
    this function changes i,j,k to coordinates by giving i,j,k values in meters.
    INPUT: XARR = xarray.dataframe 
    OUTPUT: XARR = xarray.dataframe 
    using xarray module
    """

    try:   
        #assign values to coordinates:
        # get values for i and j form xsmet, ysmet
        ival = XARR.xsmet[1::]
        jval = XARR.ysmet[1::]
        
        # assign as new variables to data
        XARR['i'] = (['i'], ival.values)
        XARR['j'] = (['j'], jval.values)
        
        # definition of attributes for new variables i,j,k
        i_attr = {'long_name' : 'i_position',
                  'axis' : 'X',
                  'units' : 'm',
                  'bounds' : 'i_bnds'}
        
        j_attr = {'long_name' : 'j_position',
                  'axis' : 'Y',
                  'units' : 'm',
                  'bounds' : 'j_bnds'}
        
        # add attributes to i,j,k in data
        XARR.i.attrs = i_attr 
        XARR.j.attrs = j_attr 
        
        print('INFO: adding i,j to ncfile')
      
    
        """
        Assign iv, jv and kv for 3D Building variables
        required if building surface variables are written on vector grid
        """
        
        if 'iv' or 'jv' in XARR.dims:
    
            ivval = XARR.xvmet
            jvval = XARR.yvmet
    
            XARR['iv'] = (['iv'], ivval.values)
            XARR['jv'] = (['jv'], jvval.values)
    
            # definition of attributes for new variables i,j,k
            iv_attr = {'long_name' : 'iv_position',
                      'axis' : 'X',
                      'units' : 'm'}
    
            jv_attr = {'long_name' : 'jv_position',
                      'axis' : 'Y',
                      'units' : 'm'}
    
            # add attributes to i,j,k in data
            XARR.iv.attrs = iv_attr 
            XARR.jv.attrs = jv_attr 
    
            print('INFO: adding iv,jv to ncfile')
            
        """
        TODO: assignment of 1D & 3D k as z or level 
        --> implemented, but needs testing
        """
        XARR = REASSIGN_VERTICAL_DIMENSIONS(XARR)
      
        """
        TODO: how to handle nsfccl. (MITRAS)
        
        try:
            print('TEST: add nsfccl to data')
            scc = ncid.nsfccl 
            XARR['scc'] = (['nsfccl'], scc.values)
        except:
            pass
        
        """
    except:
        print('INFO: REASSIGN COORDINATES was not executed. This step was skipped')
        pass
       
    return XARR
       
#=============================================================

def ASSIGN_BOUNDS( NETCDF, COORD_NAME, VALUES):
    """
    assign bound variables for coordinate variables
    using xarray module
    """
    nv = 2
    # create array
    array = np.empty((NETCDF[COORD_NAME].size, nv), 'f8')
    # assign values to array
    array[:,0] = VALUES[0:-1] 
    array[:,1] = VALUES[1::] 
    #add bounds to netCDF:
    NETCDF[COORD_NAME + '_bnds'] = ([COORD_NAME, 'nv'], array)
    NETCDF[COORD_NAME + '_bnds'].encoding = {'dtype' : 'float32', '_FillValue': None}   
    
    return NETCDF


def CREATE_BOUNDS(XARR):
    """
    assign bound variables for coordinate variables.
    Preparation for ASSIGN_BOUNDS Function.
    using xarray module
    """
    try:
        # create bounds from vector coordinates.
        # use xymet, yvmet, zvmet as bound values 
        x_bounds = XARR.xvmet
        y_bounds = XARR.yvmet
        z_bounds = XARR.zvmet[:,0,0]  #--> todo! 2d instead of array
    
        # replace nan values at last position
        x_bounds[-1] = x_bounds[-2] + (x_bounds[-2] - x_bounds[-3])
        y_bounds[-1] = y_bounds[-2] + (y_bounds[-2] - y_bounds[-3])
    
        # assign data for bounds
    
        XARR = ASSIGN_BOUNDS(XARR, 'i', x_bounds)
        XARR = ASSIGN_BOUNDS(XARR, 'j', y_bounds)
        
        if XARR.yzsurf.values.mean() == 0:
            XARR = ASSIGN_BOUNDS(XARR, 'k', z_bounds)
            print('INFO: adding i_bnds, j_bnds, k_bnds to ncfile')
        else:
            print('INFO: adding i_bnds, j_bnds to ncfile')

    except:
        print('INFO: CREATE_BOUNDS was not executed. This step was skipped')
    return XARR


#=============================================================
def ADD_TIME_ATTRS( XARR): 
    XARR.time.attrs['long_name'] = 'time'
    XARR.time.attrs['standard_name'] = 'time'
    XARR.time.attrs['axis'] = 'T'
    XARR.time.attrs['bounds'] = 'time_bnds'
    return XARR

def ASSIGN_TIME_BOUNDS(XARR):    
    """
    TODO: Add time bounds
    process 'time' and 'time bounds'
    we get the number of time steps and the averaged length of a time step,
    finally, we create a `time_bnds` (time bounds) variable and fill it with values
    """
    
    nv = 2
    val_time = XARR.time.values

    # dTime intervale
    ntime = XARR.time.size
    dtime = np.mean(val_time[1:(ntime)] - val_time[0:(ntime-1)])

    # calculate bounds
    array = np.empty((ncid.time.size, nv), 'f8')
    array[0:ntime,0] = val_time[0:ntime]-dtime/2.0
    array[0:ntime,1] = val_time[0:ntime]+dtime/2.0

    # set time bounds
    XARR['time_bnds'] = (['time', 'nv'], array)
    XARR['time_bnds'] = XARR.time_bnds.astype('datetime64[ns]')
    XARR['time_bnds'].encoding = {'_FillValue': None}   
    print('INFO: ASSIGN_TIME_BOUNDS done')

    # return XARR

#============================================================= 
    
def GEOCOORDINATES(XARR, PROJECTION, SWITCH, XREF, YREF):
    """
    Reassigning coordinates.
    old lat, lon are used to calculate UTM and geographical lat, lon coordinates
    Reference Point can be set manually otherwise using model reference point.
    Default reference Point: UTM GEOMATIKUM
    using xarray module
    """
    try:
        #--- Cartesian Coordinates (in meters)
        #--- variables lat, lon (MITRAS) are handles as x,y .
        #--- rewuired: lat(j,i), lon(j,i) 
        x_val = XARR.lon.values
        y_val = XARR.lat.values
    
        # Reference Point:
        #------------------------------
        if SWITCH == True:
            # method 1: use own coordinates XREF & YREF (assigned by User)
            pass
        else:
            # method 2: using reference point in data (assigned in GA-File)
            try: 
                # Format: dd.dddd
                elam = XARR.elam  # lon
                ephi = XARR.ephi  # lat
                # convert elam & ephi to utm
                XREF, YREF = PROJECTION(elam, ephi, inverse=False)
            except:
                XREF, YREF = 564568.279, 5935921.365
                print('INFO: GEOCOORDINATES: no reference point in dataset, using default coordinates (Geomatikum)')
                   
        # Calculate UTM coordinates
        #------------------------------
        # Recreate UTM Coordinates
        # XREF,YREF = Referencepoint in UTM, and x_val, y_val in meters
        x_utm = XREF + x_val
        y_utm = YREF + y_val
    
        # Add x_utm, y_utm to netCDF and add attributes to coordinates
        XARR['x_utm'] = (['j','i'], x_utm)
        XARR['y_utm'] = (['j','i'], y_utm)
    
        XARR.x_utm.attrs = {'long_name'     : 'easting',
                            'standard_name' : 'projection_x_coordinate',
                            'units'         : 'm'}
        XARR.y_utm.attrs = {'long_name'     : 'northing',
                            'standard_name' : 'projection_y_coordinate',
                            'units'         : 'm'}
        
        # Calculate lat lon coordinates
        #------------------------------
        # create data array for lat, lon from x_utm, y_utm
        x_dummy = XARR.x_utm.copy()
        y_dummy = XARR.y_utm.copy()
    
        # recalculate lat lon based on utm with the projection function:
        lon, lat = PROJECTION(x_dummy, y_dummy, inverse=True)
    
        # assign variables to netCDF and add attributes to coordinates
        XARR['lon'] = (('j','i'), lon)
        XARR['lat'] = (('j','i'), lat)
    
        XARR.lon.attrs = {'long_name'     : 'longitude',
                          'standard_name' : 'longitude',
                          'units'         : 'degrees_east'}
        XARR.lat.attrs = {'long_name'     : 'latitude',
                          'standard_name' : 'latitude',
                          'units'         : 'degrees_north'}
    
        print('INFO: GEOCOORDINATES: adding UTM and geographical coordinates to ncfile') 

    except:
        print('INFO: GEOCOORDINATES was not executed: lon, lat variables are missing.') 
        
    return XARR


#============================================================= 
    
def GEOCOORDINATES_VECTOR(XARR, PROJECTION, SWITCH, XREF, YREF):
    """
    Reassigning coordinates.
    old latv, latu, lonv, lonu are used to calculate UTM and geographical coordinates.
    Reference Point can be set manually otherwise using model reference point.
    Default reference Point: UTM GEOMATIKUM
    using xarray, pyproj
    """

    try:
    
        # Cartesian Coordinates (in meters)
        # variables lat, lon (MITRAS) are handles as x,y .
        xu_val = XARR.lonu.values
        xv_val = XARR.lonv.values
        yu_val = XARR.latu.values
        yv_val = XARR.latv.values
    
        # Reference Point:
        #------------------------------
        if SWITCH == True:
            # method 1: use own coordinates XREF & YREF (assigned by User)
            pass
        else:
            # method 2: using reference point in data (assigned in GA-File)
            try: 
                # Format: dd.dddd
                elam = XARR.elam  # lon
                ephi = XARR.ephi  # lat
                # convert elam & ephi to utm
                XREF, YREF = PROJECTION(elam, ephi, inverse=False)
            except:
                XREF, YREF = 564568.279, 5935921.365
                print('INFO: GEOCOORDINATES_VECTOR no reference point in dataset, using default coordinates (Geomatikum)')
                   
        # Calculate UTM coordinates
        #------------------------------
        # Recreate UTM Coordinates
        # XREF,YREF = Referencepoint in UTM, and x_val, y_val in meters
        xu_utm = XREF + xu_val
        xv_utm = XREF + xv_val
        yu_utm = YREF + yu_val
        yv_utm = YREF + yv_val
    
        # Add x_utm, y_utm to netCDF and add attributes to coordinates
        XARR['xu_utm'] = (['j','iv'], xu_utm)
        XARR['xv_utm'] = (['jv','i'], xv_utm)
        XARR['yu_utm'] = (['j','iv'], yu_utm)
        XARR['yv_utm'] = (['jv','i'], yv_utm)
    
        XARR.xu_utm.attrs = {'long_name' : 'xu-easting',
                            'units'      : 'm'}
        XARR.xv_utm.attrs = {'long_name' : 'xv-northing',
                            'units'      : 'm'}
        XARR.yu_utm.attrs = {'long_name' : 'yu-easting',
                            'units'      : 'm'}
        XARR.yv_utm.attrs = {'long_name' : 'yv-northing',
                            'units'      : 'm'}
        
        # Calculate lat lon coordinates
        #------------------------------
        # create data array for lat, lon from x_utm, y_utm
        xu_dummy = XARR.xu_utm.copy()
        xv_dummy = XARR.xv_utm.copy()
        yu_dummy = XARR.yu_utm.copy()
        yv_dummy = XARR.yv_utm.copy()
    
        # recalculate lat lon based on utm with the projection function:
        lonu, latu = PROJECTION(xu_dummy, yu_dummy, inverse=True)
        lonv, latv = PROJECTION(xv_dummy, yv_dummy, inverse=True)
    
        # assign variables to netCDF and add attributes to coordinates
        XARR['lonu'] = (('j','iv'), lonu)
        XARR['latu'] = (('j','iv'), latu)
        XARR['lonv'] = (('jv','i'), lonv)
        XARR['latv'] = (('jv','i'), latv)
    
        XARR.lonu.attrs = {'long_name' : 'u-longitude',
                          'units'      : 'degrees_east'}
        XARR.latu.attrs = {'long_name' : 'u-latitude',
                          'units'      : 'degrees_north'}    
        XARR.lonv.attrs = {'long_name' : 'v-longitude',
                          'units'      : 'degrees_east'}
        XARR.latv.attrs = {'long_name' : 'v-latitude',
                          'units'      : 'degrees_north'}
    
        print('INFO:GEOCOORDINATES_VECTOR adding vector UTM and geographical coordinates to ncfile') 
    except:
        print('INFO: GEOCOORDINATES_VECTOR was not executed: variables are missing.') 
        
    
    return XARR


#=============================================================
def SELECT_OUTPUT_VARIABLES(XARR, OWN_VAR_LIST):
    """
    Prepare output, select variables
    using xarray module
    """
    
    # get variables from file 
    varlist = list(XARR)    
    output =[]            

    # get variable_list and check against netcdf variables
    from dict_OUTPUT_variables import variable_list
    
    for var in varlist:
        if var in variable_list.values():
            output.append(var)
        else:
            pass

    #add custom variables:
    if OWN_VAR_LIST:  # check if list is not empty
        for var in OWN_VAR_LIST: 
            if not var in output: # check if var is not in output
                output.append(var)
    else: 
        pass


    #--- reduce size of netCDF if possible:
    try: 
        if  len(output) != 0:
            print('INFO: SELECT_OUTPUT_VARIABLES: available output variables:', end=' ')
            print(*output)
            return XARR[output]  
    except:   
        if len(output) == 0:
                raise Exception('WARNING: NO VARIABLES ARE PROVIDED. Please provide Output variables via dict_OUTPUT_variables or custom_variables (see USER INPUT SECTION)')
    finally:
        print('INFO: SELECT_OUTPUT_VARIABLES: all variables provided!')
        return XARR
        
    
#=============================================================
def ADD_GLOBAL_ATTRS(METADATA_TABLE):
    """
    Created by Angelika Heil
    Get columns requirements and BSH entry from excel file; 
    write into pandas dataframe
    using EXCEL-Sheet and pandas module
    """
    try:
        pdglat = pd.read_excel(open(METADATA_TABLE, 'rb'),sheet_name='data_files', header=2, nrows=40, usecols=[1, 8])
    except (RuntimeError, TypeError, NameError):
        print('ERROR: File could not be opended. Make sure you saved the Excel-File as WORKSHEET (.xlsx) and not as STRICT OPEN XML SHEET (.xlsx)')
    # Remove all rows that have NaN entry
    glat = pdglat[pdglat.iloc[:, 1].str.contains("NaN")==0]
    glat = glat.replace(to_replace=r'#', value='', regex=True)
    #history2021 = glat[(glat['Requirements'] == 'history_year2021')].iloc[0,1]  ##-- same as glat['Entry_by_user'].iloc[-1]
    dictglat  = dict(zip(glat.iloc[:-1, 0].str.strip(),glat['Entry_by_user']))   #-- except last row
    dictglat['creation_date'] = datetime.now().isoformat(timespec='seconds')
  
    print('INFO: ADD_GLOBAL_ATTRS: adding global metadata to ncfile')
    return dictglat


def ADD_GLOBAL_HISTORY_ATTRS(PATHFILE):
    """
    Adding dataset creation date and modification date to global metadata
    PATHFILE = path of file and file name
    """
    create_time= os.path.getctime(PATHFILE)
    dt_c = datetime.fromtimestamp(create_time).strftime('%a %b %d %Y')
    dt_m = datetime.now().strftime('%a %b %d %Y')
    globattr_hist = "{}: data created with with m2cdf \n{}: data standardised with nc2atmodat.py".format(dt_c,dt_m)
    return globattr_hist   


def DELETE_GLOBAL_ATTRS(XARR):
    """
    Deletes MEMI attribues
    using xarray module
    """
    
    # list global attributes, which should be removed
    del_glob_attrs = ['Model',
                      'NCO',
                      'history_of_appended_files',
                      'Convention', 
                      'Datatype',
                      'Title',
                      'Version',
                      'Institution',
                      'Person',
                      'Program',
                      'Project',
                      'Comment']  
    
    for attr in del_glob_attrs:
        if attr in list(XARR.attrs):
            del XARR.attrs[attr]
        else:
            pass

    return XARR

#=============================================================
def ADD_CUSTOM_ATTRIBUTES_TO_VARIABLES(XARR):
    """
    assign comments and corrections to variables.
    set comments in dict_MEMI_record_numbers
    using xarray module
    """
    from dict_custom_variables_attributes import custom
    
    for variable in custom:
        for key in custom[variable]:
            try:
                XARR[variable].attrs[key] = custom[variable][key]
            except Exception:
                pass
    print('INFO: ADD_CUSTOM_ATTRIBUTES_TO_VARIABLES custom attributes and comments to variables added')   
    return XARR

#=============================================================
def CELL_METHODS(XARR):
    """
    Correction of cell_methods if i,j,k are renamed to x,y,z
    """
    print('INFO: CELL_METHODS rewrite cell_methods')
    for var in XARR.variables:
        dims = XARR[var].dims
        if 'cell_methods' in XARR[var].attrs:
            try: 
                cellm = XARR[var].cell_methods
                if 'x' in dims:
                    cellm = cellm.replace('i:','x:')
                if 'y' in dims:
                    cellm = cellm.replace('j:','y:')
                if 'z' in dims:
                    cellm = cellm.replace('k:','z:')   
                if 'xv' in dims:
                    cellm = cellm.replace('iv:','xv:')
                if 'yv' in dims:
                    cellm = cellm.replace('jv:','yv:')
                if 'kv' in dims:
                    cellm = cellm.replace('k:','kv:')
                XARR[var].attrs['cell_methods'] = cellm      
            except:
                pass
    return XARR


def ADD_CELL_METHODS(XARR):
    """
    Add cell_methods if none are assigned
    Generic: time = instantaneous (point), spatial coordinates = mean
    """
    print('INFO: ADD_CELL_METHODS:')
    for var in XARR.variables:
        dims = XARR[var].dims
        if 'cell_methods' not in XARR[var].attrs:
            print(f'...create generic cell_methods attributes for variable {var}...', end='')
            if len(dims) > 0:
                if var in dims:
                    print('skipped...')
                    pass
                else:
                    cellm = (': '.join(XARR[var].dims))+':'
                    if 'time' in dims:
                        cellm = cellm.replace('time:', 'time: point')
                    if len(cellm) > 0 and cellm[-1] == ':':
                        cellm = cellm + ' mean'
                    XARR[var].attrs['cell_methods'] = cellm    
                    print(' added!')
    return XARR
        
#=============================================================

def CORRECTION_VARIABLE_ATTRIBUTES(XARR):
    """
    Formatting corrections to long/standard_names and removing empty variables.
    """
    
    print('INFO: CORRECTION_VARIABLE_ATTRIBUTES small fixes to long/standard_names and removing empty variables.')
    for var in XARR.variables:
        attributes = XARR[var].attrs
        
        # remove empty attribues
        try:
            new_attributes = {key: value for key, value in attributes.items() if value}
        except:
            pass

    # remove _ in long name attribute
    if 'long_name' in new_attributes:
        new_long_name = new_attributes['long_name'].replace("_", " ")
        new_attributes['long_name'] = new_long_name
    else:
        pass

    XARR[var].attrs = new_attributes   
    return XARR
   
    

#=============================================================

def GRID_MAPPING(XARR, PROJECTION):
    """    
    Projection  ---  TODO
    Projection and Grid mapping are required, if i,j are not lat, lon and lat, lon are not provided with the dataset.
    if variable has the attribute coordinates = 'lon lat' then grid mapping is not required.
    otherwise this is used as a calculation information for coordinate tranformation.
    adding crs can be done by pyproj
    """
    print('INFO: GRID_MAPPING')

    """
    Daniels Skript:
    Attributes for UTM
    """
    #var_lcc = ncid.createVariable(grid_mapping_variable_name, 'i4')
    #var_lcc.grid_mapping_name = "universal_transverse_mercator" ;
    #var_lcc.longitude_of_central_meridian = 9. ;
    #var_lcc.false_easting = 500000. ;
    #var_lcc.false_northing = 0. ;
    #var_lcc.latitude_of_projection_origin = 0. ;
    #var_lcc.scale_factor_at_central_meridian = 0.9996 ;
    #var_lcc.long_name = "CRS definition" ;
    #var_lcc.longitude_of_prime_meridian = 0. ;
    #var_lcc.semi_major_axis = 6378137. ;
    #var_lcc.inverse_flattening = 298.257223563 ;
    #var_lcc.spatial_ref = "PROJCS[\"WGS 84 / UTM zone 32N\",GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",9],PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"32632\"]]" ;
    #var_lcc.GeoTransform = "564931.5 3 0 5934924.5 0 -3 " ;
    
    """
    #Experimente in bash mit proj
    !echo $elam $ephi | proj +proj=utm +lat_0=53.54 +lon_0=10.005 +k_0=3.5  +ellps=WGS84 +units=m
    !echo $elam $ephi | proj +proj=tmerc +lat_0=0 +lon_0=9 +k_0=1 +x_0=3500000 +y_0=0  +ellps=WGS84 +units=m
    """ 
    
    # select CRS from Model domain coordinates.
    from pyproj.aoi import AreaOfInterest
    from pyproj.database import query_utm_crs_info

    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
           west_lon_degree= XARR.lon.min(),   
           south_lat_degree= XARR.lat.min(),  
           east_lon_degree= XARR.lon.max(),   
           north_lat_degree= XARR.lat.max(),
        ),)

    utm_crs = CRS.from_epsg(utm_crs_list[0].code)

    # write crs to netcdf
    ncid['crs'] = 'crs'
    ncid.crs['epsg_code'] = "EPSG:{}".format(utm_crs_list[0].code)
        
    #used Projection (definded in the beginning)
    p = PROJECTION
    grid_mapping_p = p.crs
    epsg = grid_mapping_p.to_authority()
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(int(epsg[1]))
    # create human-readable string
    # this is the magic right here!
    esri_pe_string = proj.ExportToWkt()

    
    # return XARR
#=============================================================
  

    
    
    
