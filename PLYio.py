# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:15:12 2017

@author: Alexander Wolff  :)
"""


#Tuple List: Converts list of list into list of tuples
def tuple_list( list_list ):
    tuple_list =list()
    
    for item in list_list:
        tuple_list.append( tuple(item) )
        
    return tuple_list

#Gets header of .PLY file : returns list of strings
def get_ply_header(filename, end_header = "end_header"):
    #open file in reading mode
    file_contents = open(filename, 'r')
    
    #prepare container
    header = list()
    
    #reset buffer
    line = ""
    
    #sentinel
    count = 0
    
    #while enf of header is not encountered : append
    while(line[0:10] != end_header):
        line = file_contents.readline()
        header.append( line.split() )
        
        if(count > 1000):
            print("Error : No end of Header detected")
            break
        else:
            count+=1
    
    #close file
    file_contents.close()
    
    return header

#Extracts dtype information from header into dtype format required for PLY conversion
def extract_dtype( header ):
    
    #Lookup-table
    dtype_lookup = { 'float':'f4', 'uchar':'u1', 'float32':'f4', 'uint8':'u1', 'int':'u1' }
    
    #prepare container
    dtype = list()
    
    #extract properties as tuples
    for line in header:
        if( line[0] == "property" ):
            dtype.append( (line[2], dtype_lookup[line[1]]) ) 

    return dtype

#Modifies vertex & num_cols to given number
def modify_ply_header( header, vertex ):
    new_header = list()
    
    for item in header:
        
        if(len(item)<3): 
            continue
        
        if((item[1] == 'vertex') or (item[1] == 'num_cols')):
            item[2] = str(vertex)
        
        new_header.append(item)
        
    return new_header

#Converts header data into a string ready to write out
def ply_header_tostring(header):
     
    #Head
    str_header = ['ply']
    
    for item in header:
        str_header.append(' '.join(item))
    
    #Tail
    str_header.append('end_header')
    
    return '\n'.join(str_header)+'\n'

#Writes dataframe to file using template
def dataframe_to_ply(templatefile, dataframe, filepath, verbose=False):
    import time
    
    #Verbose
    if(verbose):
        print("[IO] Writing "+filepath)
        start = time.time()
    
    #Get header
    header = get_ply_header(templatefile)
    header = modify_ply_header(header, len(dataframe) )
    header = ply_header_tostring(header)
    
    #Make sure colours are of int type
    for i in [3,4,5]:
        dataframe[i] = dataframe[i].astype('int')
    
    #Write header
    with open(filepath, 'w') as newfile:
        newfile.write( header )
    
    #Write file
    dataframe.to_csv(filepath, sep = ' ', index = False, header = None, mode = 'a')
    
    #Verbose
    if(verbose):
        end = time.time()
        print("[IO] Completed in "+ str(end-start) + " seconds")

#Writes dataframe to file in PLY format
def write_ply( original_file, new_file, dataframe, verbose = False, binary=True ):
    #imports
    import plyfile, numpy, time
    
    #ASCII text format
    if(not binary):
        dataframe_to_ply( original_file, dataframe, new_file, verbose=verbose )
        
    else:
        
        #Verbose
        if(verbose):
            print("[IO] Writing "+new_file)
            start = time.time()
        
        #read template
        header = get_ply_header( original_file )
        template_dtype = extract_dtype( header )
    
        #Verbose
        if(verbose):
            point_a = time.time()
            print("[IO][A] Read Template in {0} seconds".format(point_a - start))
    
        #Convert Dataframe into PLY object
        tuples = tuple_list( dataframe.values.tolist() )
        data_array = numpy.array( tuples, dtype = template_dtype)
        data_ply = plyfile.PlyElement.describe( data_array, 'vertex' )
        
        #Verbose
        if(verbose):
            point_b = time.time()
            print("[IO][B] Converted DataFrame into PLY object in {0} seconds".format(point_b - point_a))
        
        #Write PLY object to file
        plyfile.PlyData([data_ply], text=False).write(new_file)
        
        #Verbose
        if(verbose):
            point_c = time.time()
            print("[IO][C] Wrote PLY object to file in {0} seconds".format(point_c - point_b))
        
        #Verbose
        if(verbose):
            end = time.time()
            print("[IO] Completed in "+ str(end-start) + " seconds")
    
#Loads PLY file into dataframe
def read_ply( filename, verbose = False ):
    #imports
    import time, pandas, plyfile
        
    #Verbose
    if(verbose):
        print("[IO] Loading "+filename)
        start = time.time()

    #Load File
    try:
        #Counts rows to ignore
        header = get_ply_header( filename )
        skip_length = len(header)
    
        #Load File : faster if data is not binary
        dataframe = pandas.read_csv(filename, skiprows=skip_length, sep=' ', header=None)
    
    except:
        #Load File
        plydata = plyfile.PlyData.read( filename )
        dataframe = pandas.DataFrame(plydata.elements[0].data)

    #Verbose
    if(verbose):
        end = time.time()
        print("[IO] Completed in "+ str(end-start) + " seconds")
        
    return dataframe
