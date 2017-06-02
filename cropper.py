#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 15:27:26 2017

@author: Alexander Wolff
"""

#used in development
debug = False


#Imports
import time, sys

#Local Libraries
import statistics, PLYio, UI


#UI arguments    
arguments = UI.get_arguments( default_sample_size = 10000  )
arguments = UI.dealwith_arguments( arguments, sys.argv )


#Linking File Path
if(debug):
    path = r'C:\Users\Alexander Wolff\Desktop\Virtual'
    filenames = ['odm_georeferenced_model', "awebery-house", "st-michael", "helipix_roof"]
    filename = filenames[1]
    
    pointcloud_csv_file = path + '\\'+ filename +'.csv'
    pointcloud_ply_file = path + '\\'+ filename +'.ply'

    arguments['input-file']['data'] = pointcloud_ply_file


#Parsing
arguments['sigma']['data'] = float(arguments['sigma']['data'])
arguments['sample-size']['data'] = int(arguments['sample-size']['data'])
arguments['data-limit']['data'] = int(arguments['data-limit']['data'])

#Verbose
verbose = arguments['verbose']['flag']
if(verbose):
    print("[INPUT] Input File:        {}".format( arguments['input-file']['data']) )
    print("[INPUT] Output File:       {}".format( arguments['output-file']['data']) )  
    print("[INPUT] Standard Deviation:{}".format( arguments['sigma']['data']))
    print("[INPUT] Sample Size:       {}".format( arguments['sample-size']['data']) )
    print("[INPUT] Data-Point Limit:  {}".format( arguments['data-limit']['data'] )  )
    print("[INPUT] Binary Output:     {}".format( arguments['binary-output']['flag']))
    print("[INPUT] Plot:              {}".format( arguments['plot']['flag']) )
    print("[INPUT] Verbose:           {}".format( arguments['verbose']['flag']) )

    start_total = time.time()
    print("[MAIN] Starting Program : {}".format(time.asctime()))
    

#Loading Data
pointcloud_data = PLYio.read_ply( arguments['input-file']['data'], verbose=verbose )

#Random Sample Small Dataset
sample_data = statistics.sample_dataset( pointcloud_data, arguments['sample-size']['data'],  label="small", verbose=verbose )

#Select large dataset size
if( arguments['data-limit']['data'] > (len(pointcloud_data)-1)):
    large_data_size = len(pointcloud_data)-1
else:
    large_data_size = arguments['data-limit']['data']
                             
#Random Sample Large Dataset
large_data  = statistics.sample_dataset( pointcloud_data, large_data_size,      label="large", verbose=verbose )

#Crop Within 2 Sigma
if( arguments['plot']['flag'] ):
    print("[WARNING] Having the plot graph open will halt the cropping process. Please close the graphs to resume cropping.")   
cropped_sample = statistics.fast_crop(large_data, sample_data, sigma=arguments['sigma']['data'], verbose=verbose, columns=[0,1], algorithm='gauss',plot=arguments['plot']['flag'])

#Write File
PLYio.write_ply( arguments['input-file']['data'], arguments['output-file']['data'], cropped_sample, verbose=verbose, binary=arguments['binary-output']['flag'])

#Verbose
if(verbose):
    end_total = time.time()
    print("[MAIN] Total Process Time: "+ str(end_total-start_total) + " seconds")
    print("[MAIN] Exiting Program : {}".format(time.asctime()))
    
#END
sys.exit(0)

 