
from MultiHex.core import load_map, save_map

from math import sqrt
from numpy import save, load, ndarray
from numpy.random import rand 

import os

def _is_valid_texture(obj,which):
    """
    Checks the object provided to verify that it is a properly formated texture list
    """
    if not (isinstance(obj, list) or isinstance(obj, ndarray)):
        print("Not List, {}".format(type(obj)))
        return(False)
    if not (isinstance(obj[0], list) or isinstance(obj[0],ndarray)):
        print("Not List, {}".format(type(obj[0])))
        return(False)
    if not (len(obj)==len(obj[0])):
        print("Not rectangular")
        return(False)
    
    if which=='rectangular':
        if not (isinstance(obj[0][0], float) or isinstance(obj[0][0], int)):
            print("Not number")
            return(False)
    elif which=='gradient':
        if not (isinstance(obj[0][0], list)):
            print("Does not contain list-entries")
            return(False)
        else:
            if not (isinstance(obj[0][0][0], float) and isinstance(obj[0][0][1], float)):
                print("One or both entries not a list")    
                return(False)
    else:
        print("dat no good")
        return(False)
    return(True)

def _save_texture(obj,which='rectangular'):
    """
    Saves the texture to a numpy file and also ensures it is a properly formated texture list
    """
    assert(_is_valid_texture(obj, which))
    where = os.path.join(os.path.dirname(__file__),'.texture.npy')
    save( where, obj)

def _load_texture():
    """
    Loads the saved texture and verifies that it is valid before returning it
    """
    where = os.path.join(os.path.dirname(__file__),'.texture.npy')
    temp = load(where)
    return( temp )


def _interpolate( start, end, weight):
    """
    Linear interpolation between two points 
    """
    return( start + weight*(end - start) )

def _dot_grid_gradient( gridx, gridy, posx, posy, texture):
    """
    Calculates the dot product between a grid-vertex's Gradient vector AND the distance vector from that vertex to a given position
    """
    # optionally, the user can pass the texture itself to minimize IO
   
    if not _is_valid_texture(texture,'gradient'):
        raise ValueError("Something was wrong with the specified texture")
    
    dx = posx - float(gridx)
    dy = posy - float(gridy)
   
    return( dx*texture[gridx][gridy][0] + dy*texture[gridx][gridy][1] )

def _generate_gradients( size = 128 ):
    """
    Generates a square grid with a unit-vector at each vertex, and saves it to a numpy file. 
    """
    # first we need to instantiate the list and roll dice for the gradient vectors
    grads = [[ [rand(),0] for i in range(size) ] for j in range(size)]

    # then we need to calculate the y-component of the gradient vectors 
    # this process is slow. Some implementations use a hash-lookup table.
    for i in range(size):
        for j in range(size):
            grads[i][j][1] = sqrt( 1- grads[i][j][0] )

    _save_texture( grads, 'gradient')



def _generate_perlin_texture(size = 512):
    """
    This generates a texture from which to sample in the perlinize function. 
    """
    assert(isinstance(size, int))
    assert( size % 2 == 0 )

    # we need a 2D array of points which will represent our noise texture
    #    later, we will sample from this texture by interpolating between points on it
    grid_full = [ [rand() for j in range(size)] for i in range(size) ]

    # now we need some down-sampled maps to apply large-scale fluctuations

    # So first we find the maximum number of downsamples we can perform
    levels = 1
    while (size % (2**levels) ==0):
        levels += 1
    levels-=1
    print("Doing {} levels of down-sampling".format(levels))

    downsamples = {}
    for level in range(levels):
        eff_size = int(size/(2**(level+1)))
        downsamples[ level ] = [ [rand() for j in range(eff_size)] for i in range( eff_size ) ]


    # now we go add all the layers together
    for i in range(size):
        for j in range(size):
            for level in range(levels):
                eff_size = int(size/(2**(level+1)))
                eff_i = int(i/(2**(level+1))) 
                eff_j =  int(j/(2**(level+1)))
                grid_full[i][j] += 0.6*((level+1)**1)*downsamples[level][ eff_i ][ eff_j ]

                grid_full[i][j] += 0.1*((level+1)**1)*( downsamples[level][ (eff_i+1)%eff_size ][ eff_j ] \
                                + downsamples[level][ eff_i   ][ (eff_j+1)%eff_size ] \
                                + downsamples[level][ (eff_i-1)%eff_size ][ eff_j ] + downsamples[level][ eff_i ][ (eff_j-1)%eff_size ]  )

    maax = max(grid_full)
    miin = min(grid_full)
    for i in range(size):
        for j in range(size):
            grid_full[i][j] = 2*((grid_full[i][j]- miin)/(maax - miin)) - 1

    _save_texture(grid_full)

def _grad_sample( xsam, ysam, x_pos, y_pos, scale, texture):
    x_pos_scale = x_pos*scale
    y_pos_scale = y_pos*scale

    x_weight = x_pos_scale - xsam
    y_weight = y_pos_scale - ysam

    n0 = _dot_grid_gradient( xsam, ysam, x_pos_scale, y_pos_scale ,texture)
    n1 = _dot_grid_gradient( xsam+1, ysam, x_pos_scale, y_pos_scale ,texture)
    ix0 = _interpolate( n0, n1, x_weight)

    n0 = _dot_grid_gradient( xsam, ysam+1, x_pos_scale, y_pos_scale ,texture)
    n1 = _dot_grid_gradient( xsam+1, ysam+1, x_pos_scale, y_pos_scale ,texture)
    ix1 = _interpolate( n0, n1, x_weight)
    return( _interpolate( ix0, ix1, y_weight ))

def sample_noise(x_pos, y_pos, xsize=None, ysize=None, texture=None, algorithm='gradient'):
    """
    Samples from a texture list-object by interpolating between points in its 2D array. This is done by treating the two indices of the texture as (x,y) coordinates.
    When a point between those integer indices is requested, the average of the values corresponding to the indices that are floor and roof of that point are used.

    When an xsize and ysize are specified, we stretch the provided x_pos and y_pos to fit within the texture's bounds by treating the x/ysize as the maximum index of the texture. 

    params
    x_pos   - float, the x position at which to sample
    y_pos   - float, the y position at which to sample

    """

    # optionally, the user can pass the texture itself to minimize IO
    if texture is None:
        try:
            texture = _load_texture()
        except IOError:
            print("File not found while sampling. Generating...")
            if algorithm=='rectangular':
                _generate_perlin_texture()
            elif algorithm=='gradient':
                _generate_gradients()
            else:
                raise NotImplementedError("Unsupported algorithm: {}".format(algorithm))
            texture = _load_texture()
    if not _is_valid_texture(texture, algorithm):
        raise ValueError("Something was wrong with the specified texture")

    # we need to stretch the texture to fit the map
    if xsize is None:
        xscale_factor = 1.
    else:
        assert( isinstance(xsize,float) or isinstance(xsize,int))
        xscale_factor = float(len(texture))/xsize
    if ysize is None:
        yscale_factor = 1.
    else:
        yscale_factor = float(len(texture[0]))/ysize

    abs_scale = min([ xscale_factor, yscale_factor])

    # get the lower corner in the texture that the requested position is closest to
    xsam = int(x_pos*abs_scale)
    ysam = int(y_pos*abs_scale)

    # we need to be sure we're sampling within the bounds of the texture
    if not (xsam < len(texture) and xsam>=0):
        raise ValueError("Position {} is beyond the extent {}".format(xsam, len(texture)))
    if not (ysam < len(texture[0]) and ysam>=0):
        raise ValueError("Position {} is beyond the extent {}".format(ysam, len(texture[0])))
    
    if algorithm=='rectangular':
        # now just average the pixels around the sampled point
        value = texture[xsam][ysam] + texture[(xsam+1)%len(texture)][ysam] + texture[xsam][(ysam+1)%len(texture[0])] + texture[(xsam+1)%len(texture)][(ysam+1)%len(texture[0])]
        return( 0.25*value)
    elif algorithm=='gradient':
        temp =  _grad_sample(xsam, ysam, x_pos, y_pos, abs_scale, texture)
        temp += _grad_sample(xsam, ysam, x_pos, y_pos, abs_scale/10., texture)

def perlinize( which = os.path.join(os.path.dirname(__file__),'..','saves','generated.hexmap'), algorithm='gradient', attr='_altitude_base', magnitude = 0.20 ):
    """
    Injets perline noise into the specified map's attribute. 

    @param which - which map. Either a string specifying the filepath or a pointer to the Hexmap
    @param attr  - which hex attribute to modify 
    @param magnitude - scale of noise to inject. 0.05-0.40
    """
    
    # this opens the map / loads the map to the proper variable 
    if isinstance(which,str):
        main_map = load_map(which)
    #elif isinstance(which, Hexmap):
    #    main_map = which
    else:
        raise TypeError("Unexpected type for arg 'which': {}. Expected {} or {}".format(type(which), str, Hexmap))


    # should ensure that the attribute given and the magnitude are appropriately typed
    if not isinstance( attr, str ):
        raise TypeError("Unexpected type {} for arg 'str', expected {}".format(type(attr), str))
    if not isinstance(magnitude, float):
        raise TypeError("Expected {} for 'magnitude', got {}".format(float, type(magnitude)))
    
    # We need to make sure the attribute exist in our Hexes! This way we don't waste time creating a texture we don't need 
    for HexID in main_map.catalogue:
        if hasattr( main_map.catalogue[HexID], attr):
            break
        else:
            raise KeyError("HexMap does not have attribute {}".format(attr))

    # We need to create a noise texture file
    if algorithm=='rectangular': 
        _generate_perlin_texture()
    elif algorithm=='gradient':
        _generate_gradients()
    else:
        raise NotImplementedError("Unsupported algorithm {}".format(algorithm))
    # then grab it into an object to minimize IO later on
    texture = _load_texture()
    for HexID in main_map.catalogue:
        this_hex = main_map.catalogue[HexID]
        cent = this_hex.center
        # use the Hexes location to skew the specified attribute of the hex 
        new_value = getattr(this_hex, attr) + magnitude*sample_noise(cent.x, cent.y, main_map.dimensions[0], main_map.dimensions[1], texture)
        setattr( this_hex, attr, new_value)
        this_hex.rescale_color()
    save_map( main_map, which )



