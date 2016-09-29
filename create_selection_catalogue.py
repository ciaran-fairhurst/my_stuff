#Creates a catalogue of all the properties used in our selection process for finding EELS

#import modules
import numpy as np
import os
import utilities as u
from astropy.io import fits


data_dir = '/home/ciaran/Desktop/Workstuff/My_Code/GAMAII/Catalogues/'

tables = {}
tables['GaussFitSimplev05']=fits.open(data_dir + 'GaussFitSimplev05.fits')[1].data
LambdarCat = fits.open('../../Catalogues/LambdarCatv01.fits')[1].data
LambdarList = []
for i,line in enumerate(LambdarCat):
    if i%500==0: print i
    LambdarList.append( line[0] )

output = []
output_cols = ['CATAID','SPECID','Z','HA_EW','HA_FLUX','HA_EW_ERR','HA_FLUX_ERR']


for i,k in enumerate(output_cols):
    output.append('# '+str(i+1)+' '+k+'\n')

j=0
for i,CATAID in enumerate(tables['GaussFitSimplev05']['CATAID']):
    if i%10 ==0:  print i, j

    if CATAID in LambdarList:
        SPECID = tables['GaussFitSimplev05']['SPECID'][i]

        o = {}
        o['CATAID'] = CATAID
        o['SPECID'] = SPECID
        o['Z'] = tables['GaussFitSimplev05']['Z'][i]

        try:
            o['HA_EW'] = float(tables['GaussFitSimplev05']['HA_EW'][i])
            o['HA_EW_ERR'] = float(tables['GaussFitSimplev05']['HA_EW_ERR'][i])
            o['HA_FLUX'] = float(tables['GaussFitSimplev05']['HA_FLUX'][i])
            o['HA_FLUX_ERR'] = float(tables['GaussFitSimplev05']['HA_FLUX_ERR'][i])

        except IndexError:
            for k in output_cols[2:]:
                o[k] = '-99.99'



        out_str = ''
        for k in output_cols:
            out_str += str(o[k])+' '

        output.append(out_str+'\n')
        j+=1
    else:
        pass

candidates=open('catalogues/selection.cat','w')
candidates.writelines(output)
