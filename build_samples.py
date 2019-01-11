 #////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
# script: build_samples.py
# authors: Lincoln Harris
# date: 1.11.19
#
# Building samples.csv, with pandas...would have been better to do 
# this with jupyter, but not working on VM, for some reason
#
# usage:
#		ipython build_samples.py
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

	files = os.listdir(path) 
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

	files = os.listdir(path) 
	for f in files:
		try:
			if f.endswith('R2_001.fastq.gz'):
				retStr = path + '/' + f 
				return retStr
		except IndexError:
			return 'dummy'

#////////////////////////////////////////////////////////////////////
# main()
#	
#////////////////////////////////////////////////////////////////////

cwd = os.getcwd()

bucketPrefixes = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/'
f = 'bucketPrefixes.txt'
get_ipython().system('aws s3 ls $bucketPrefixes > $f')

# read run prefixes into a pandas df
runs_df = pd.read_table(f, delim_whitespace=True, header=None, names=['is_prefix', 'run_name'])

# add a full_path col
runs_df['full_path'] = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/' + runs_df['run_name']
#print(runs_df)

for i in range(0, len(runs_df.index)-1): # want to account for STAR-fus_out prefix
	global prefix
	prefix = runs_df['full_path'][i]
	print(prefix)

	currRun = runs_df['run_name'][i]
	print('downloading s3 files')
	get_ipython().system('aws s3 cp $prefix ./$currRun --recursive --quiet')

	cellsList = os.listdir(cwd + '/' + currRun)

	# read cellsList into a pandas df
	cells_df = pd.DataFrame({'cell_name':cellsList})

	# add a full_path col
	cells_df['full_path'] = cwd + '/' + currRun + cells_df['cell_name']

	# add input_fq1/2 cols
	cells_df['input_fq1'] = cells_df['full_path'].map(get_fastqs_R1) 
	cells_df['input_fq2'] = cells_df['full_path'].map(get_fastqs_R2) 

	samples_df = cells_df[['cell_name', 'input_fq1', 'input_fq2']]

	print(currRun)
	print('writing samples file')
	outFileName = 'samples_' + currRun.strip('/') + '.csv'
	samples_df.to_csv(outFileName, index=False, sep='\t', header=False)
	print('	')

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
