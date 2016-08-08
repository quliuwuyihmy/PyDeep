''' This class contains some example toy problems for RBMs.

    :Implemented:
        - Bars and Stripes dataset
        - Shifting bars dataset
        - 2D mixture of Laplacians

    :Version:
        1.0

    :Date:
        06.06.2016

    :Author:
        Jan Melchior

    :Contact:
        JanMelchior@gmx.de

    :License:

        Copyright (C) 2016 Jan Melchior

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
import numpy as numx 
import pydeep.base.numpyextension as npExt

def generate_2D_mixtures(num_samples, 
                         mean = 0.0, 
                         scale = numx.sqrt(2.0) / 2.0):
    ''' Creates a dataset containing 2D data points from a random mixtures of
        two independent Laplacian distributions.
     
    :Info:
        Every sample is a 2-dimensional mixture of two sources. The sources 
        can either be super_gauss or sub_gauss. If x is one sample generated 
        by mixing s, i.e. x = A*s, then the mixing_matrix is A.

    :Parameters:
        num_samples: The number of training samples.
                    -type: int
                     
        mean:        The mean of the two independent sources.
                    -type: float
                     
        scale:       The scale of the two independent sources.
                    -type: float

    :Returns:
        Data and mixing matrix
       -type: list of numpy arrays ([num samples, 2], [2,2])

    '''
    source = numx.concatenate( (numx.random.laplace(mean, scale, 
             num_samples), numx.random.laplace(mean, scale, num_samples)) 
             ).reshape(num_samples, 2, order = 'F') 
    mixing_matrix = numx.random.rand(2,2) - 0.5
    mixture = numx.dot(source, mixing_matrix.T)
    return mixture, mixing_matrix

def generate_bars_and_stripes(length, 
                              num_samples):
    ''' Creates a dataset containing samples showing bars or stripes.
    
    :Parameters:
        length:      Length of the bars/stripes.
                    -type: int
                
        num_samples: Number of samples
                    -type: int
        
    :Returns:
        Samples
       -type: numpy array [num_samples, length*length]
        
    '''
    data = numx.zeros((num_samples,length*length))
    for i in range(num_samples):
        values = numx.dot(numx.random.randint(low = 0, high = 2,
                                              size=(length,1)),
                                              numx.ones((1,length)))
        if(numx.random.random()>0.5):
            values = values.T
        data[i,:] = values.reshape(length*length)
    return data

def generate_bars_and_stripes_complete(length):
    ''' Creates a dataset containing all possible samples showing bars or 
        stripes.
    
    :Parameters:
        length: Length of the bars/stripes.
               -type: int
        
    :Returns:
        Samples
       -type: numpy array [num_samples, length*length]
        
    '''
    stripes = npExt.generate_binary_code(length)
    stripes = numx.repeat(stripes, length, 0)
    stripes = stripes.reshape(2**length,length*length)

    bars = npExt.generate_binary_code(length)
    bars = bars.reshape(2**length*length,1)
    bars = numx.repeat(bars, length, 1)
    bars = bars.reshape(2**length,length*length)
    return numx.vstack((stripes[0:stripes.shape[0]-1],bars[1:bars.shape[0]]))

def generate_shifting_bars(length, 
                           bar_length, 
                           num_samples, 
                           random = False, 
                           flipped = False):
    ''' Creates a dataset containing random positions of a bar of length 
        "bar_length" in a strip of "length" dimensions.
    
    :Parameters:
        length:      Number of dimensions
                    -type: int
                
        bar_length:  Length of the bar
                    -type: int
                 
        
        num_samples: number of samples to generate
                    -type: int
                    
        random:      If true dataset gets shuffled
                    -type: bool
        
        flipped:     If true dataset gets flipped 0-->1 and 1-->0 
                    -type: bool     
        
    :Returns:
        Complete shifting bars dataset
       -type: numpy array [samples, dimensions]
        
    ''' 
    data = numx.zeros((num_samples,length))
    for i in range(0,num_samples):
        index = numx.random.randint(0,length)
        for b in range(0,bar_length):
            data[i][(index+b)%length] = 1.0
    if random:
        numx.random.shuffle(data)
    if flipped:
        data = (data + 1) % 2
    return data

def generate_shifting_bars_complete(length, 
                                    bar_length, 
                                    random = False, 
                                    flipped = False):
    ''' Creates a dataset containing all possible positions of a bar of 
        length "bar_length" can take in a strip of "length" dimensions.
    
    :Parameters:
        length:     Number of dimensions
                   -type: int
                
        bar_length: Length of the bar
                   -type: int
                    
        random:     If true dataset gets shuffled
                   -type: bool
        
        flipped:    If true dataset gets flipped 0-->1 and 1-->0 
                   -type: bool     
        
    :Returns:
        Complete shifting bars dataset
       -type: numpy array [samples, dimensions]
        
    '''
    data = numx.zeros((length,length))
    for i in range(0,length):
        for b in range(0,bar_length):
            data[i][(i+b)%length] = 1
    if random:
        numx.random.shuffle(data)
    if flipped:
        data = (data + 1) % 2
    return data
