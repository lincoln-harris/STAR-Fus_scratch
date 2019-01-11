#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
# script: build_samples.py
# authors: Lincoln Harris
# date: 1.11.19
#
# Building samples.csv, with pandas...would have been better to do 
# this with jupyter, but not working on VM, for some reason
#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
import os
import json
import pandas as pd
pd.options.display.max_colwidth = 500 # module config? 
pd.options.mode.chained_assignment = None  # disable warning message? -- really shouldnt be doing this...

#////////////////////////////////////////////////////////////////////
# get_fastqs_R1()
#      get full local path, for fq1
# 
#////////////////////////////////////////////////////////////////////
def get_fastqs_R1(path):

	files = os.listdir(path + '/') 
	for f in files:
		try:
			if f.endswith('R1_001.fastq.gz'):
				retStr = path + '/' + f
				return retStr
		except IndexError:
			return 'dummy'

#////////////////////////////////////////////////////////////////////
# get_fastqs_R2()
#      get full local path, for fq1
# 
#////////////////////////////////////////////////////////////////////
def get_fastqs_R2(path):

	files = os.listdir(path + '/') 
	for f in files:
		try:
			if f.endswith('R2_001.fastq.gz'):
				retStr = path + '/' + f
				#print(retStr)
				return retStr
		except IndexError:
			return 'dummy'

#////////////////////////////////////////////////////////////////////
# main()
#	
#////////////////////////////////////////////////////////////////////

cwd = os.getcwd()

f = 'cellNames.txt'
get_ipython().system('ls {cwd}/170202/ > $f')

# read cell names into a pandas df
cells_df = pd.read_table(f, delim_whitespace=True, header=None, names=['cell_name'])

# add a full_path col
cells_df['full_path'] = cwd + '/' + '170202/' + cells_df['cell_name']

# add input_fq1/2 cols
cells_df['input_fq1'] = cells_df['full_path'].map(get_fastqs_R1) 
cells_df['input_fq2'] = cells_df['full_path'].map(get_fastqs_R2) 
print(cells_df)

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
