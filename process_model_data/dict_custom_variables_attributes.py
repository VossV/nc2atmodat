#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Created on Fri Mar 26 2021
#@author: Vivien Voss

#===============================================
#   Variables with special description
#-----------------------------------------------
# This function can be used to add corrections to variable attributes
# please add variable and attributes as dictionaries and add the variable
# to the second dictionary
#
# EXAMPLE:
#---------------------------------------------------------------------------------------------
#'my_var' : {'long_name'     : 'example long name',          
#            'standard_name' : 'example_standard_name' #'INFO: CF should_only_be_assigned_if_standard_name_exists_in_CF',
#            'units'         : 'm s-1'
#            'comment'       : 'this is an example entry'}

#---------------------------------------------------------------------------------------------
#--- Step 1: Define individual variables entries and attributes
#----------

conc01 = {'long_name'      : 'concentration of pm10',          
          'standard_name'  : 'mass_concentration_of_pm10_ambient_aerosol_particles_in_air',
          'units'          : 'kg m-3'}

ahoru = {'comment' : 'horizontal exchange coefficient for momentum/TKE'}

averu = {'comment' : 'vertical exchange coefficient for momentum/TKE'}

fzdl  = {'comment' : 'The Monin Obukhov Stability parameter is a dimensionless length parameter used in boundary layer meteorology to parameterize fluxes in the surface layer. It defined as the ratio of the reference (measurement) height (z) and the Obukhov length scale (L). Reference: Srivastava et al. 2017, https://doi.org/10.1007/s10546-017-0273-y.' }

nsfccl = {'comment' : 'Identifier for each surface cover class used in this model domain. This variable is related to surface variables.'}

qvrf2m = {'comment' :'2m relative humidity'}

t2m    = {'comment' : '2m temperature is calculated by interpolating between the lowest model level and the Earth\'s surface, taking account of the atmospheric conditions'}

ustern = {'comment' : 'friction velocity' }   

elam = {'comment'   : ''}

ephi = {'comment'   : ''}

zvmet = {'long_name'     : 'height above mean sea level',
         'standard_name' : 'height_above_mean_sea_level',
         'comment'       : 'height of the vertical grid cell boundary, lowest layer denotes the orography height'}  #aendern: 'vertical distance above surface" in m2cdf

zsmet = {'long_name'     : 'height above mean sea level',
         'standard_name' : 'height_above_mean_sea_level',
         'comment'       : 'height of the vertical grid cell centre'}  #aendern: 'vertical distance above surface" in m2cdf

tbuisurf_e = {'comment': 'Surface temperature at eastern building wall '}
tbuisurf_w = {'comment': 'Surface temperature at western building wall '}
tbuisurf_n = {'comment': 'Surface temperature at northern building wall '}
tbuisurf_s = {'comment': 'Surface temperature at southern building wall '}
tbuisurf_t = {'comment': 'Surface temperature at buidling roof '}
tbuisurf_b = {'comment': 'Surface temperature at building ceiling '}
tbuisurf_p = {'comment': 'Plane view of surface temperature at building roof '}

bqlract_e = {'comment': 'Surface rain water rate at eastern building wall '}
bqlract_w = {'comment': 'Surface rain water rate at western building wall '}
bqlract_n = {'comment': 'Surface rain water rate at northern building wall '}
bqlract_s = {'comment': 'Surface rain water rate at southern building wall '}
bqlract_t = {'comment': 'Surface rain water rate at buidling roof '}
bqlract_b = {'comment': 'Surface rain water rate at building ceiling '}
bqlract_p = {'comment': 'Plane view of surface rain water rate at building roof '}

bqlrdel_e = {'comment': 'Surface rain water amount at eastern building wall '}
bqlrdel_w = {'comment': 'Surface rain water amount at western building wall '}
bqlrdel_n = {'comment': 'Surface rain water amount at northern building wall '}
bqlrdel_s = {'comment': 'Surface rain water amount at southern building wall '}
bqlrdel_t = {'comment': 'Surface rain water amount at buidling roof '}
bqlrdel_b = {'comment': 'Surface rain water amount at building ceiling '}
bqlrdel_p = {'comment': 'Plane view of surface rain water amount at building roof '}

bqlrint_e = {'comment': 'Surface rain water at eastern building wall '}
bqlrint_w = {'comment': 'Surface rain water at western building wall '}
bqlrint_n = {'comment': 'Surface rain water at northern building wall '}
bqlrint_s = {'comment': 'Surface rain water at southern building wall '}
bqlrint_t = {'comment': 'Surface rain water at buidling roof '}
bqlrint_b = {'comment': 'Surface rain water at building ceiling '}
bqlrint_p = {'comment': 'Plane view of surface rain water at building roof '}

#---------------------------------------------------------------------------------------------
#--- Step 2: add the variable to the collection
#----------
custom = { 'conc01' : conc01, 
           'ahoru'  : ahoru,
           'averu'  : averu, 
           'fzdl'   : fzdl,
           'nsfccl' : nsfccl,
           'qvrf2m' : qvrf2m, 
           't2m'    : t2m,
           'ustern' : ustern,
           'elam'   : elam,
           'ephi'   : ephi,
           'zvmet'  : zvmet,
           'tbuisurf_e':  tbuisurf_e,
           'tbuisurf_w':  tbuisurf_w,
           'tbuisurf_n':  tbuisurf_n,
           'tbuisurf_s':  tbuisurf_s,
           'tbuisurf_t':  tbuisurf_t,
           'tbuisurf_b':  tbuisurf_b,
           'tbuisurf_p':  tbuisurf_p,
           'bqlract_e' :  bqlract_e,           
           'bqlract_w' :  bqlract_w,         
           'bqlract_n' :  bqlract_n,          
           'bqlract_s' :  bqlract_s,         
           'bqlract_t' :  bqlract_t,         
           'bqlract_b' :  bqlract_b,         
           'bqlract_p' :  bqlract_p,
           'bqlrdel_e' :  bqlrdel_e,
           'bqlrdel_w' :  bqlrdel_w,
           'bqlrdel_n' :  bqlrdel_n,
           'bqlrdel_s' :  bqlrdel_s,
           'bqlrdel_t' :  bqlrdel_t,
           'bqlrdel_b' :  bqlrdel_b,
           'bqlrdel_p' :  bqlrdel_p,
           'bqlrint_e' :  bqlrint_e,
           'bqlrint_w' :  bqlrint_w,
           'bqlrint_n' :  bqlrint_n,
           'bqlrint_s' :  bqlrint_s,
           'bqlrint_t' :  bqlrint_t,
           'bqlrint_b' :  bqlrint_b,
           'bqlrint_p' :  bqlrint_p
         }
