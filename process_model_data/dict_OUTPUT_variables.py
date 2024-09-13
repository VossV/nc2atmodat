#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 2021
@author: Vivien Voss

===============================================================================
 This file should contain a list of variables that are used in the 
 corresponding model system.
 Variables are stored in python-dictionaries.
===============================================================================

-------------------------------------------------------------------------------
how to call a Dictionary: 
-------------------------
  Dict_name[key] --> value
  - key: record number
  - value: variable name

Example:
  variable_list['18b_rec'] should return 'elam'

-------------------------------------------------------------------------------
Adding new variables:
---------------------
  If you want to add a record number containing multiple variables,
  please distinguish each entry.

  example: rec. no 11 contains xvmet and yxmin.
			'11' : 'xvmet'
			'11' : 'yxmin'
  calling key '11' will only return the last entry (yxmin), 
  and not xvmet.
	
  current solution: add letters to the rec.no: 
			'11a' : 'xvmet'
			'11b' : 'yxmin'

"""
#==============================================================================
#  RECOMMENDED   variables
###############################################################################

coordinate_list = {
 'a' : 'lat',
 'b' : 'lon',
 'c' : 'i',
 'd' : 'j',
 'e' : 'k',
 'f' : 'x_utm',
 'g' : 'y_utm',
 'h' : 'i_bnds',
 'i' : 'j_bnds',
 'j' : 'k_bnds',
 'k' : 'x',
 'l' : 'y',
 'm' : 'z',
 'n' : 'x_bnds',
 'o' : 'y_bnds',
 'p' : 'z_bnds'
}

#==============================================================================
# variable_list (initially based on MITRAS/METRAS variables)
#==============================================================================
variable_list ={
#'1'   : 'zeit',    # Switches
'2'   : 'nsfccl',  # Switches
#'4'   : 'ntrace',     # Switches
#'4'   : 'nxyq',
#'8'   : 'nm50scc',
'10a_rec' : 'albedo',
#'10b_rec' : 'qvdeep',
#'11a' : 'xvmet',
#'11b' : 'yxmin',
#'12a' : 'yvmet',
#'12b' : 'yymin',
#'13a' : 'yztop',
'13a_rec'  : 'zvmet',
'13b_rec'  : 'zsmet',
'17_rec'  : 'yzsurf',
#'18a' : 'edrewi',
'18b_rec' : 'elam',
'18c_rec' : 'elat',
'18d_rec' : 'elon',
'18e_rec' : 'ephi',
'19_rec'  : 'surfra',
#'52'  : 'ereducv',
#'59a' : 'nsurfcells',
#'59b' : 'nsurfcount',
#'59c' : 'nsurfdir',
#'59d' : 'nsurftype',
#'59e' : 'nxobst',
#'59f' : 'nyobst',
#'59g' : 'nzobst',
#'81'  : 'ntindx',
# '1000a' : 'zeit',
# '1000b' : 'time_step_number',        # jn
# '1000c' : 'time_step_length',        # dt
'1010_rec'  : 'building_mask',         # vol, (n3dobst)
'1100_rec'  : 'qvcont',                
'1900a_rec' : 'yz0t',                  # yz0
'1900b_rec' : 'surfrat',               # surfra
# '1901'  : 'albedo_ice',
# '1902'  : 'yz0h2o',
# '1903'  : 'yz0theta',
# '2000'  : 'xv_wind',                 # 'ut',  # (old name: UJN)
'2003_rec'  : 'x_wind',                # 'uts',
# '2020'  : 'ut_init',
# '2100'  : 'yv_wind',                 # 'vt',  # (Old name: VJN)
'2103_rec'  : 'y_wind',                # 'vts',
# '2120'  : 'vt_init',
'2200_rec'  : 'z_wind',                # 'wt',  # (Old name WJN)
# '2220'  : 'wt_init',
# '2301'  : 'ff',
# '2302'  : 'dd',
# '2601'  : 'rotor_mask',      
# '2604'  : 'uturb',          
# '2605'  : 'poweroutput_rotor',
# '2606'  : 'power_cp',
'3400_rec'  : 'P_total',
'4003_rec'  : 'rhosum',
#'5003'  : 'ztpsum',
#'5005'  : 'zvtpsum',
 '5006_rec'  : 'treal',
 '5101_rec'  : 'tmrt',
 '5102_rec'  : 'utci',
 '5103_rec'  : 'pet',
 '5104_rec'  : 'pt',
# '5800'  : 'nsolzeit',
# '5900_rec'  : 'tbuisurf',
 '5901a'      : 'tbuisurf_e',
 '5901b'      : 'tbuisurf_w',
 '5901c'      : 'tbuisurf_n',
 '5901d'      : 'tbuisurf_s',
 '5901e'      : 'tbuisurf_t',
 '5901f'      : 'tbuisurf_b',
 '5902'      : 'tbuisurf_p',
# '5905'  : 'btflx',
 '5910_rec'  : 'sfcbnets',
 '5911_rec'  : 'sfcbnetl',
 '5912_rec'  : 'sfcbinl',
 '5913_rec'  : 'sfcbgskyl',
 '5914_rec'  : 'sfcbgroul',
# '5915'  : 'wturbu',
# '5916'  : 'wcondu',
# '5917'  : 'sfcboutl',
# '5918'  : 'sfcbouts',
# '5919'  : 'sfcbwalll',
# '5920'  : 'sfcbinssky',
 '5921_rec'  : 'sfcbins',
# '5922'  : 'sfcinlsky',
 '6000_rec'  : 'averu',
 '6001_rec'  : 'ahoru',
# '6010'  : 'averphi',
# '6011'  : 'avhorphi',
# '6020'  : 'wdev',
 '6051_rec'  : 'tkesum',
# '6052'  : 'rmixl',
# '6060'  : 'dist',
# '6061'  : 'dissum',
# '6500'  : 'ustern',
# '6501'  : 'tstern',
# '6502'  : 'fzdl',
# '6503'  : 'qvstern',
# '6550'  : 'momfl',
# '6551'  : 'hfl',
# '6553'  : 'vfl',
# '6554'  : 'hflpt',
# '6560'  : 'qanth',
 '6600_rec'  : 'ujstern',
 '6601_rec'  : 'tjstern',
 '6602_rec'  : 'qvjstern',
# '6603'  : 'surblh',
 '6650_rec'  : 'tjjnb',
 '6651_rec'  : 'qvjjnb',
# '6653'  : 'tbreal',
# '6700'  : 'zinv',
# '6710'  : 'wstern',
# '7003'  : 'zqvsum',
# '7005'  : 'bqvflx',
 '7006_rec'  : 'rh',
 '7103_rec'  : 'qlcsum',
# '7105'  : 'bqlcflx',
 '7203_rec'  : 'qlrsum',
# '7205'  : 'bqlrflx',
# '7209'  : 'qlrsedi',
 '7210'   : 'qlract',
 '7211_rec'  : 'qlrdel',
# '7212_rec'  : 'qlrint',
# '7214'  : 'bqlrdel',
# '7215'  : 'bqlrint',
# '7217a'  : 'bqlract_e',
# '7217b'  : 'bqlract_w',
# '7217c'  : 'bqlract_s',
# '7217d'  : 'bqlract_n',
 '7217e'  : 'bqlract_t',
# '7217f'  : 'bqlract_b',
 '7217g'  : 'bqlract_p',
# '7218a'  : 'bqlrdel_e',
# '7218b'  : 'bqlrdel_w',
# '7218c'  : 'bqlrdel_s',
# '7218d'  : 'bqlrdel_n',
 '7218e'  : 'bqlrdel_t',
# '7218f'  : 'bqlrdel_b',
 '7218g'  : 'bqlrdel_p',
# '7219a'  : 'bqlrint_e',
# '7219b'  : 'bqlrint_w',
# '7219c'  : 'bqlrint_s',
# '7219d'  : 'bqlrint_n',
# '7219e'  : 'bqlrint_t',
# '7219f'  : 'bqlrint_b',
# '7219g'  : 'bqlrint_p',
# '7300'  : 'cool',
# '7301'  : 'heat',
# '7400'  : 'sfcnetl',
# '7401'  : 'sfcnets',
# '7402'  : 'swdo',
# '7403'  : 'swup',
# '7404'  : 'sjnetl',
# '7405'  : 'sjnets',
# '7406'  : 'sglob',
# '7407'  : 'slbod',
# '7408'  : 'slgeg',
# '7410'  : 'swdodif',
# '7411'  : 'swdodir',
# '7415'  : 'sfcinssky',
# '7416'  : 'lwdo',
# '7417'  : 'lwup',
#'7505'  : 't2m',                      # Fehlerhaft
#'7507'  : 'qvrf2m',                   # Fehlerhaft
#'7510'  : 'sepiWs',
#'7511'  : 'sepjiWpm2',
#'8000_rec'  : 'conc'                  # 5D variable, macht probleme bei CDO, NCO etc.
'8001'   : 'conc01',                   #----> Alternative zu conc
'8002'   : 'conc02',                   #----> Alternative zu conc
'8100_rec'  : 'ssvd',
#'8101   : 'ssvd',
'8200_rec'  : 'sssdel',
#'8202   : 'sssdel',
'8300_rec'  : 'sssint',
#8301    : 'sssint',
'8400_rec'  : 'sssedi',
'8401_rec'  : 'sssint',
'8500_rec'  : '??',
'8600_rec'  : 'sswdel',
'8700_rec'  : 'sswint',
'9000_rec'  : 'ssq',
#'12000' : 'u0no',
#'12100' : 'v0no',
#'12200' : 'w0no',
'13400'  : 'p0no',
'15003'  : 't0no',
'17003'  : 'qv0no',
'17103'  : 'qlc0no',
'18500'  : 'ss0no'	
#'99000' : 'userfield',
}

###############################################################################
variable_list.update(coordinate_list)



