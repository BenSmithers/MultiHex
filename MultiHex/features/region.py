try:
    from numpy import cos, sin
except ImportError:
    from math import cos, sin

class Region:
    """
    A Region is a collection of Hexes on a Hexmap
    """

    def __init__(self, hex_id, parent):
        self.enclaves = [  ]
        self.ids = [ hex_id ]
        self.name = ""
        
        self.parent_map = parent
        
        self.perimeter = self.parent_map.catalog[hex_id]._vertices

    def merge_with_region( self, other_region ):
        """
        Takes another region and merges it into this one.

        """
        #TODO: prepare a write up of this algorithm 

        # determine if Internal or External region merge
        internal = False  # is 
        n_borders = 0

        # we need to start on the beginning of a border, so we get the first point that's on the border
        start_index = 0
        while self.perimeter[start_index] not in other_region.perimeter:
            start_index+=1 
            if start_index==len(self.perimeter): #if we've gotten all the way around, break
                internal = True
                break
        
        # if we found a border on the perimeter, this is an external type merge
        if start_index!=len(self.perimeter):
            internal = False

        # count the number of borders, find the "starting points" for the new enclaves and perimeter
        on_border = False
        start_indices = []
        for point in range(len(self.perimeter)):
            if self.perimeter[ (point+start_index)%len(self.perimeter) ] in other_region.perimeter:
                if not on_border:
                    on_border = True
                    n_borders += 1
            else:
                if on_border:
                    start_indices.append( (point+start_index)%len(self.perimeter)) 
                    on_border = False
            

        if not internal:
            loops = [glom( self.perimeter, other_region.perimeter, index ) for index in start_indices]
            found = False
            new_encalves = []
            for loop in loops:
                if self.get_shape_type( loop ) == 1:
                    if found:
                        raise Exception(" This should be impossible ")
                    found = True
                    self.perimeter = loop
                else: # type 2
                    new_enclaves.append( loop )
            
        else:
            # need to find the enclave this other region is bordering 
            found_enclave = False
            for enclave in self.enclave:
                start_index = 0
                while enclave[start_index] not in other_region.perimeter:
                    start_index+= 1
                    if start_index==len(enclave):
                        # does not border this enclave 
                        break
                if start_index==len(enclave):
                    # let's go to the next one
                    continue
                
                # if the new region borders two distinct enclaves, there needs to be overlap between the regions, and this method is broken
                assert( not found_enclave )
                found_enclave = True
                
                # same as before, we walk around 
                start_indices = []
                on_border = False
                for point in range(len( enclave )):
                    if enclave[ (point + start_index)%len(enclave) ] in other_region.perimeter:
                        if not on_border:
                            on_border = True
                    else:
                        if on_border:
                            start_indices.append( ( point + start_index) % len(enclave ))
                            on_border = False

                # that old enclave is split into multiple new enclaves (or even just one)
                self.enclaves.pop( self.enclaves.index( enclave ) )
                self.enclaves += [ glom( enclave, other_region.perimeter, index) for index in start_indices ] 


        # these are just added on in
        self.enclaves   += other_region.enclaves 
        self.ids        += other_region.ids
    

    def add_hex_to_region( self, other_hex ):
        """
        Adds a hex to this region
        """
        
        # plugs an enclave?
        # closes part of the perimeter and creates an enclave? 
        pass
        
    def pop_hex_from_region( self, pop_hex ):
        """
        Pops a hex from this region
        """
        
        # Creates an enclave, try merging it with enclaves or perimeter 
        # 
        
        pass

    
    def get_shape_type( self, shape ):
        """
        Returns "Type" of a closed shape

        Type 1 - shape encloses a  region. By walking clockwise around a type 1 shape, hexes to the right will be in the region.
        Type 2 - shape encloses an enclave. By walking clockwise around a type 2 shape, hexes to theright will *not* be in the region.
        """

        point_1 = shape[0]
        point_2 = shape[1] # "clockwise" is, by convention, adding one to the index 

        step_vec = point_2 - point_1
        right_point = step_vec + Point( self.parent._drawscale*cos( step_vec.angle - 90), self.parent._drawscale*sin( step_vec.angle - 90 ))
        that_id = self.parent.get_id_from_point( right_point )

        if that_id in self.ids:
            return( 1 )
        else:
            return( 2 )


def glom( original, new, start_index ):
    """
    Partially gloms two perimeters together. This part is being written for the External Type merge

    Used to grab one of the new enclaves and the new perimeter 
    """

    new_perimeter = []
    
    index = start_inex 
    while original[ index % len(original) ] not in new:
        new_perimeter += original[ index % len(original) ]
        index += 1

    intersect_index = new.index( original[index % len(original)] )

    while new[ index % len(new) ] not in original:
        new_perimeter += new[index % len( new) ]
        index -= 1 #going counterclockwise

    intersect_index = original.index( new[index % len(new)])
    
    index = intersect_index 
    while (index % len(original) != start_index ):
        new_perimeter += [ original[index % len(original)]]
        index +=1 

    return( new_perimeter )



def merge(group_vertices, other_vertices, shift=False):
    """
    Takes two lists of points, each interpreted as a closed shape. The two need to share a border. 

    Returns a list of points representing the merged perimeter
    """
    new_vertices = []
    
    start_index = 0
    while group_vertices[ start_index ] in other_vertices:
        start_index+=1
        if len(start_index)==group_vertices:
            return(other_vertices)

    iterator = start_index

    # walk along to the right until you hit an intersect, accumulating points as you go
    while group_vertices[iterator % len(group_vertices) ] not in other_vertices:
        new_vertices += [group_vertices[iterator % len(group_vertices)]]
        iterator+=1
        if abs(iterator-start_index) >= len(group_vertices):
            raise Exception("Regions share no border")
    
    new_vertices += [group_vertices[iterator %len(group_vertices)]]

    # now we're at a branching point! 
    step_dir = 1
    intersect_index = other_vertices.index( group_vertices[iterator % len(group_vertices)] )

    if (other_vertices[ (intersect_index + 1) % len(other_vertices) ] not in group_vertices) and (other_vertices[ (intersect_index - 1) % len(other_vertices) ] not in group_vertices):
        raise Exception("Shouldn't be possible")
    
    # if the point to the right is on the original border, continue left
    # if the point to the left is on the original border, continue right
    if other_vertices[ (intersect_index + 1) % len(other_vertices) ] not in group_vertices:
        step_dir = 1
    elif other_vertices[ (intersect_index - 1) % len(other_vertices) ] not in group_vertices:
        setp_dir = -1
    else:
        raise Exception("A lone intersection should be impossible!")

    # switch over to the new border, collecting vertices until you reach another intersection
    iterator = intersect_index + step_dir
    while other_vertices[ iterator % len(other_vertices) ] not in group_vertices:
        new_vertices += [other_vertices[iterator % len(other_vertices) ]]
        iterator += step_dir 

        if (abs(iterator - intersect_index) >= len(other_vertices)):
            raise Exception("Something bad happened")
    
    new_vertices += [ other_vertices[ iterator % len(other_vertices)]]
    intersect_index = group_vertices.index( other_vertices[ iterator  % len(other_vertices)] )
    iterator = intersect_index + 1

    # swtich to the original border, walk along in the original direction until you reach the starting point 
    while group_vertices[iterator % len(group_vertices)] != group_vertices[0]:
        new_vertices+= [group_vertices[iterator % len(group_vertices )]]
        iterator += 1
        
        if ( abs( iterator - intersect_index) >= len(group_vertices)):
            raise Exception(" Something Really bad happened")
    
    return( new_vertices )

