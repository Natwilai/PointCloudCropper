# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:07:35 2017

@author: Alexander Wolff
"""

##Random Projection
def random_projection( dataset, n_elements = 1000 ):
    #imports
    import random, pandas
    
    #Create a non-repeating list of n random elements with value ranging from 0 to length of data
    sample_indices = random.sample( range( len(dataset-1) ), n_elements )
    
    #Return random sample of length n taken from input dataset
    return pandas.DataFrame( dataset.values[sample_indices] )

##Random Sample
def random_sample( dataframe, n_elements = 1000, plot = True ):
    #imports
    import matplotlib.pyplot as pyplot    
    
    #random projection
    sample = random_projection( dataframe, n_elements )
    
    if(plot):
        #Graph
        sample[0].plot(kind='density', color='r')
        pyplot.show()
        sample[1].plot(kind='density', color='g')
        pyplot.show()
        sample[2].plot(kind='density', color='b')
    
    return sample

##Generate Density
def generate_density( input_list, n_elements = 1000, plot = True, normalise = False ):
    #imports
    import scipy.stats as stats, numpy, matplotlib.pyplot as pyplot
    
    #Caclculate density function
    density = stats.gaussian_kde(input_list)
    
    #Find workspace
    workspace = numpy.linspace( min(input_list), max(input_list), n_elements )
    
    density_function = density(workspace)
    
    if(normalise):
        density_function = density_function/max(density_function)
    
    if(plot):
        pyplot.plot(workspace, density_function)
    
    return density_function, workspace

##Calculate the Mean of input dataset
def calculate_mean( input_list ):
    
    return sum(input_list) / len( input_list )
    
##Calculate the deviation of input dataset
def calculate_deviation( input_list ):
    
    mean = calculate_mean( input_list )
    
    deviation = list()
    
    for element in input_list:
        deviation.append( (element - mean ) )

    return deviation

##Calculate Varience of input dataset
def calculate_variance( input_list ):
    
    mean = calculate_mean( input_list )
    
    variance = list()
    
    for element in input_list:
        variance.append( (element - mean )**2 )

    return sum(variance)/len(variance)

##Calculate Standard Deviation of input dataset
def calculate_standard_deviation( input_list, n_elements = 1000, plot = True, label = "", verbose = False ):
    
    #imports
    import numpy, matplotlib.pyplot as pyplot, time
    
    #Verbose
    if(verbose):
        print("[MATH] Calculating Standard Deviation "+label)
        start = time.time()
    
    #Find mean
    mean = calculate_mean( input_list )
    
    #Find deviation
    deviation = calculate_deviation( input_list )
    
    #Standard deviation = square_root( variance )
    standard_deviation = numpy.sqrt(calculate_variance( input_list ))
    
    #Find dataset deviation in terms of standard deviation
    deviation = deviation / standard_deviation
    
    #Generate density data
    generate_density( deviation, n_elements, plot, normalise = True )
    
    if(plot):
        pyplot.title(label)
        pyplot.show()
    
    #Verbose
    if(verbose):
        end = time.time()
        print("[MATH] Completed in "+ str(end-start) + " seconds")
    
    return standard_deviation, mean

##Calculate Standard Deviation of input dataset
def calculate_standard_deviation_values( input_list, n_elements = 1000, plot = True, label = "", verbose = False ):
    
    #imports
    import numpy, matplotlib.pyplot as pyplot, time
    
    #Verbose
    if(verbose):
        print("[MATH] Calculating Standard Deviation "+label)
        start = time.time()
    
    #Find mean
    mean = calculate_mean( input_list )
    
    #Find deviation
    deviation = calculate_deviation( input_list )
    
    #Standard deviation = square_root( variance )
    standard_deviation = numpy.sqrt(calculate_variance( input_list ))
    
    #Find dataset deviation in terms of standard deviation
    deviation = deviation / standard_deviation
    
    #Generate density data
    density, workspace = generate_density( deviation, n_elements, plot, normalise = True )
    
    if(plot):
        pyplot.title(label)
        pyplot.show()
    
    #Verbose
    if(verbose):
        end = time.time()
        print("[MATH] Completed in "+ str(end-start) + " seconds")
    
    return standard_deviation, mean, density, workspace


##Calculate Origianl Value using Standard Deviation and Mean
def regenerate_value( value, standard_deviation, mean ):
    return (value * standard_deviation) + mean


#Crop Min Max : only keep data within (Min < x < Max) boundaries
def crop_min_max( data, column, min_value, max_value):
    
    data = data[data[column] > min_value]
    data = data[data[column] < max_value]
    
    return data

#Fast crop : uses sample data to calculate sigma, returns cropped data in large dataset
def fast_crop(large_data, sample_data, sigma, columns = [0,1], verbose = False, algorithm = 'gauss',plot=False):
    #imports
    import time
    
    #Verbose
    if(verbose):
        print("[MATH] Cropping Dataset to "+ str(sigma) + " sigma")
        start = time.time()
        
    #Crop within selected columns' sigma boundaries 
    for i in columns:
        if(algorithm == 'density'):
            _, min_value, max_value = crop_within_standard_deviation( sample_data[i], sigma )
            
        elif(algorithm == 'gauss'):
            std, mean, density, workspace = calculate_standard_deviation_values( sample_data[i], n_elements=len(sample_data),plot=False)
            min_value, max_value = gaussian_plot(density, workspace, multiplier=sigma, plot=plot)
            min_value = regenerate_value(min_value, std, mean)
            max_value = regenerate_value(max_value, std, mean)
            
        large_data = crop_min_max( large_data, i, min_value, max_value)
    
    #Verbose
    if(verbose):
        end = time.time()
        print("[MATH] Completed in "+ str(end-start) + " seconds")
    
    return large_data

#Crop within standard deviation : calculate min/max values to crop dataset within specified sigma
def crop_within_standard_deviation( input_list, sigma, plot=False ):
    
    standard_deviation, mean = calculate_standard_deviation( input_list, plot=plot )
    
    min_value = ((-1 * sigma) * standard_deviation) + mean
    max_value = (sigma * standard_deviation) + mean

    cropped_list = list()
    
    for element in input_list:
        
        if( (element > min_value) and (element < max_value) ):
            cropped_list.append(element)
            
    generate_density( cropped_list, plot=plot )
            
    return cropped_list, min_value, max_value

#Sample dataset
def sample_dataset( dataset, sample_size, label = "", verbose = False ):
    #imports
    import time
    
    #Verbose
    if(verbose):
        print("[MATH] Sampling "+label+" dataset : "+ str(sample_size)+" elements")
        start = time.time()
        
    #Sampling
    sample = random_sample( dataset, sample_size, False)
    
    #Verbose
    if(verbose):
        end = time.time()
        print("[MATH] Completed in "+ str(end-start) + " seconds")
        
    return sample

def crop_within_sigma( data, sigma ):
    _, x0_min, x0_max = crop_within_standard_deviation( data[0], sigma )
    _, x1_min, x1_max = crop_within_standard_deviation( data[1], sigma )
    
    data = data[ data[0] > x0_min ]
    data = data[ data[0] < x0_max ]
    
    data = data[ data[1] > x1_min ]
    data = data[ data[1] < x1_max ]
    
    return data

#Gaussian Function
def gauss(x, *p):
    import numpy
    
    A, mu, sigma = p
    return A*numpy.exp(-(x-mu)**2/(2.*sigma**2))

#Gaussian Function
def gaussian(x, p):
    import numpy
    
    A, mu, sigma = p
    return A*numpy.exp(-(x-mu)**2/(2.*sigma**2))
  
#Plots Gradient of input function
def gradient_plot(x, y, multiplier = 1.0):
    import numpy, matplotlib.pyplot as pyplot
    
    gradient = numpy.gradient(x)
    
    max_value = x[gradient.argmax()]
    min_value = x[gradient.argmin()]
    
    figure, axes = pyplot.subplots(1,2)                            
    
    axes[0].plot(y, x, '-b',
                [max_value, max_value],  [min(x), max(x)], '--r', 
                [min_value, min_value],  [min(x), max(x)], '--r' )
    
    axes[1].plot(y, gradient, 
                [max_value, max_value],  [min(gradient), max(gradient)], '--r', 
                [min_value, min_value],  [min(gradient), max(gradient)], '--r' )
    
    pyplot.show()
    pyplot.figure()
    
def gaussian_plot(x, y, multiplier = 2.0, plot = False):
    import matplotlib.pyplot as pyplot, scipy
    
    parameters, _ = scipy.optimize.curve_fit( gauss, y, x, p0=[1.0,0.0,1.0] )
    _,_,sigma = parameters
    
    
    max_value = sigma* multiplier
    min_value = sigma*-multiplier
    
    if(plot):
        pyplot.plot(y, x, '-b',
                     y, gaussian(y,parameters), '-g',
                    [max_value, max_value],  [min(x), max(x)], '--r', 
                    [min_value, min_value],  [min(x), max(x)], '--r' )
        
        
        pyplot.title("Gaussian Fit")
        pyplot.show()
        pyplot.figure()
    
    return min_value, max_value