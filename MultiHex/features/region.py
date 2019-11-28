try:
    from numpy import cos, sin
except ImportError:
    from math import cos, sin

class Region:
    """
    A Region is a collection of Hexes on a Hexmap

    **Fuck this shit**
    """

    def __init__(self, hex_id, parent):
        self.enclaves = [  ]
        self.ids = [ hex_id ]
        self.reg_id = 0
        self.name = ""
        
        self.parent_map = parent
        
        # may throw KeyError! That's okay
        self.perimeter = self.parent_map.catalog[hex_id]._vertices

    def merge_with_region( self, other_region ):
        """
        Takes another region and merges it into this one.

        """
        #TODO: prepare a write up of this algorithm 

        # determine if Internal or External region merge
        internal = False  # is 

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
                

        if not internal: #external merge!  
            # count the number of borders, find the "starting points" for the new enclaves and perimeter
            on_border = False   
            start_indices = []
            for point in range(len(self.perimeter)):
                if self.perimeter[ (point+start_index)%len(self.perimeter) ] in other_region.perimeter:
                    if not on_border:
                        on_border = True
                else:
                    if on_border:
                        start_indices.append( (point+start_index)%len(self.perimeter)) 
                        on_border = False

            loops = [glom( self.perimeter, other_region.perimeter, index ) for index in start_indices]
            found = False
            max_x = None
            which = None
            # the perimeter loop will, of course, have a greater extent in every direction. So we just find the loop which goes the furthest in x and know that's the perimeter
            #   all the other loops are enclaves 
            for loop in loops:
                for point in loop:
                    if max_x is None:
                        max_x = point.x
                    else:
                        if point.x>max_x:
                            max_X = point.x
                            which = loop
            self.perimeter = which 
            for loop in loops:
                if loop!=which:
                    self.enclaves += loop

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
    
    def cut_region_from_self( self, other_region):
        for ID in other_region.ids:
            if ID in self.ids:
                self.pop_hexid_from_self( ID )

        
    def pop_hexid_from_self( self, hex_id ):
        """
        Pops a hex from this region

        Why was this the hardest thing to write in all of MultiHex... 
        """

        which = None
        for each in range(len( self.ids )):
            if hex_id==self.ids[each]:
                break
                which=each
        if which is None:
            raise ValueError("id not in region")
       
        self.ids.pop( which )
        
        # countable number of cases
        #    1. hex shares no border with either perimeter or any enclave: popped and made into enclave
        #    2. hex _only_ shares border with perimeter: glom perimeter to hex
        
        this_hex = self.parent.main_map.catalog[ hex_id ]
        hex_perim = this_hex[::-1]

        # check perimeter

        outer_hex = False
        for point in self.perimeter:
            if point in hex_perim:
                outer_hex = True
                break
        
        enclave_start_points = []
        # check the enclaves
        for enclave in self.enclaves:
            index = 0
            while index <len(enclave) :
                if (enclave[index] in hex_perim) and (enclave[(index + 1) % len(enclave)] not in hex_perim):
                    # note the hex indices where we'll switch to an enclave, and also note which enclave to switch to! 
                    enclave_start_points.append( [ hex_perim.index( enclave[index] ), enclave ] )
                    break
                index += 1


        # It is now known whether the hex is on the outer rim or within the region
        if outer_hex:
            new_perim = []

            # walk around the outer perimeter until we get to a point 
            start_index = 0
            while self.perimeter[start_index] not in hex_perim:
                start_index += 1

            index = start_index
            while self.perimeter[index % len(self.perimeter)] not in hex_perim:
                new_perim.append( self.perimeter[ index % len( self.perimeter) ] )
                index += 1
            new_perim.append( self.perimeter[ index % len( self.perimeter) ] )

            hex_index = hex_perim.index( self.perimeter[index]%len(self.perimeter) ) + 1 

            while hex_perim[hex_index % len(hex_perim)] not in self.perimeter:
                
                # check if this is the beginning of a thingy
                loop_complete = False
                for possibility in enclave_start_points:
                    if possibility[0]==(hex_index % len(hex_perim)):
                        new_perim.append( hex_perim[possibility[0]])
                        enclave_counter = possibility[1].index( hex_perim[possibility[0]] ) + 1

                        while possibility[1][ enclave_counter % len(possibility[1]) ] not in hex_perim:
                            new_perim.append( possibility[1][ enclave_counter % len(possibility[1])] )
                            enclave_counter += 1
                        
                        hex_index = hex_perim.index( possibility[1][ enclave_counter % len(possibility[1])] )
                        loop_complete = True
                        break
                if not loop_complete:
                    new_perim.append( hex_perim[ hex_index % len(hex_perim)] )
                    hex_index += 1
            
            index = self.perimeter.index( hex_perim[hex_index % len(hex_perim)] )
            while (index % len(self.perimeter))!=start_index:
                new_perim.append( self.perimeter[index % len(self.perimeter)])
                index+=1
            
            self.perimeter = new_perim
            for possibility in enclave_start_points:
                self.enclaves.pop( self.enclaves.index( possibility[1] ) )
            
        else:
            # internal placement. Perimeter will remain unchanged! 
            # will be adding an enclave (may merge 2-3 enclaves into 1)
            # already have all of those neighbor enclaves! 
            # popping internal hex. This will probably be a lot like the other case 
            hex_start = 0
            while( hex_perim[hex_start % len(hex_perim)] not in [part[0] for part in enclave_start_points] ):
                hex_start += 1
            
            new_enclave = []
            counter = hex_start
            while True:
                loop_complete = False
                for part in enclave_start_points:

                    if ( counter % len(hex_perim)) == part[0]:
                        new_enclave.append( hex_perim[ part[0] ] )
                        enclave_counter = part[1].index( hex_perim[part[0]] ) + 1
                        while part[1][ enclave_counter % len( part[1] )] not in hex_perim:
                            new_enclave.append( part[1][enclave_counter % len(part[1])]) 

                        counter = hex_perim.index( part[1][ enclave_counter % len( part[1] )] )
                
                        new_enclave.append( hex_perim[ (hex_start + counter) % len(hex_perim) ] )
                        loop_complete = True
                if not loop_complete:
                    counter += 1
                    new_enclave.append( hex_perim[ counter % len(hex_perim)])
                if (counter%len(hex_perim))==hex_start:
                    break
                
                # each of the old enclaves that we found need tobe popped
                for part in enclave_start_points:
                    self.enclaves.pop( self.enclaves.index( part[1] ))

                self.enclaves.append( new_enclave )

        

def glom( original, new, start_index):
    """
    Partially gloms two perimeters together.

    Walks clockwise around one perimeter, switches to the other, walks more, switches back, and eventually forms a closed loop. 
    """

    new_perimeter = []
    
    index = start_inex 
    while original[ index % len(original) ] not in new:
        new_perimeter += original[ index % len(original) ]
        index += 1

    # returns index for start of border on "new" loop 
    intersect_index = new.index( original[index % len(original)] )


    while new[ index % len(new) ] not in original:
        new_perimeter += new[index % len( new) ]
        index += 1

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

