# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 16:41:02 2017

@author: Alexander Wolff
"""

def get_arguments(default_sample_size):
    import sys
    return  {
            'input-file'    :{
                                'switches':['-i', '--input-file'],     
                                'flag':False, 
                                'index':-1,
                                'description':"Path to the input file, only .PLY format is supported.", 
                                'data':""
                              }, 
            'output-file'   :{
                                'switches':['-o', '--output-file'],    
                                'flag':False, 
                                'index':-1,
                                'description':"(optional) Path to the output file, if not specified '_cropped' will be appended to the original file name",
                                'data':""
                             },
            'help'          :{
                                'switches':['-h', '--help'],           
                                'flag':False, 
                                'index':-1,
                                'description':"Summons this help text",
                                'data':None
                             },
            'sample-size'   :{
                                'switches':['-S', '--sample-size'],    
                                'flag':False, 
                                'index':-1,
                                'description':"(optional) Size of the sample used to calculate density graphs. Default Value: {}".format(default_sample_size),
                                'data':default_sample_size
                             },
            'data-limit'    :{
                                'switches':['-d', '--data-limit'],     
                                'flag':False, 
                                'index':-1,
                                'description':"",
                                'data':sys.maxint
                             },
            'plot'          :{
                                'switches':['-p', '--plot'],           
                                'flag':False, 
                                'index':-1,
                                'description':"",
                                'data':None
                             },
            'verbose'       :{
                                'switches':['-v', '--verbose'],        
                                'flag':False, 
                                'index':-1,
                                'description':"(optional) Displays regular status messages. Turned Off by default.",
                                'data':None
                             },
            'binary-output' :{
                                'switches':['-b', '--binary-output'],
                                'flag':False,
                                'index':-1,
                                'description':"(optional) Saves output .PLY file in binary format; may save write time, is smaller in size and faster to load into other programs. Turned Off by default.",
                                'data':None
                            },
            'sigma'         :{
                                'switches':['-s', '--sigma', '--standard-deviation'],
                                'flag':False,
                                'index':-1,
                                'description':"Standard deviation by which to crop the input dataset by.",
                                'data':1.0
                            },
            }
       
        
#UI functions
def check(switches, system_arguments):
    for switch in switches:
        for i, argument in enumerate(system_arguments):
            if(argument == switch):
                return True, i
    return False, -1
                
def get_data(index, system_arguments):
    import sys
    data_index = index+1
    
    if(data_index >= len(system_arguments)):
        print("Flag was set but not used!")
        sys.exit(3)
    else:
        return system_arguments[data_index]
    
    
def dealwith_arguments(arguments, system_arguments):
    import sys, os.path
    
    for key in arguments:
        arguments[key]['flag'], arguments[key]['index'] = check( arguments[key]['switches'], system_arguments )
    
        if( (arguments[key]['data']!=None) and (arguments[key]['flag'])):
            arguments[key]['data'] = get_data( arguments[key]['index'], system_arguments )
        

    #Help
    if( arguments['help']['flag'] ):
        print("\n[HELP]\n\n")
        
        for key in arguments.keys():
            print("{}\t{}\n-------------------------------\n{}\n\n\n".format(key, arguments[key]['switches'], arguments[key]['description']))
        
        sys.exit();
    
    #Input File
    if( arguments['input-file']['flag'] ):
        
        input_file = arguments['input-file']['data']
        
        if(not os.path.isfile(input_file)):
            print("[ERROR] Could NOT find file: \"{}\" \tFile does not exist ".format(input_file))
            print("[ERROR] Abort")
            sys.exit(11)
        
        input_file_extension = input_file.split('.')[-1]
        if( not input_file_extension.upper() == 'PLY'):
            print("[ERROR] File extention {} not recognised - only .PLY is supported".format(input_file_extension))
            print("[ERROR] Abort")
            sys.exit(12)
        
    else:
        print("[ERROR] NO Input File Detected!")
        print("[MAIN] Abort")
        sys.exit(10)
        
    if( not arguments['sigma']['flag']):
        print("[ERROR] No standard deviation / sigma was selected for the cropping process.")
        print("[ERROR] Abort")
        sys.exit(13)
        
    #Output File
    if( not arguments['output-file']['flag'] ):
         arguments['output-file']['data'] =  arguments['input-file']['data'].split('.')[0]+"_cropped.ply"

    return arguments