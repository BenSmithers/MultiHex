from MultiHex.generator import make_ridges
from MultiHex.generator import fill_land
from MultiHex.generator import sim_weather
from MultiHex.generator import region_maker
from MultiHex.generator import draw_rivers

import os

"""
Provides macros for running the simulation chain

@ ridge onward - assumes the file already has defined 'ride-lines' and so skips the first step
@ full sim     - runs the entire simulation chain

both refer to the file `config.json` for simulation parameters 
"""


def ridge_onward( size, name ):
    fill_land.generate( size, name )
    sim_weather.generate( size, name )
    draw_rivers.generate(size, name)
    region_maker.generate( size, name )

def full_sim( size, name ):
    make_ridges.generate( size, name )
    ridge_onward( size, name )

if __name__=='__main__':
    full_sim( 'cont', os.path.join( os.path.dirname(__file__), '..', 'saves', 'generated.hexmap' ))
