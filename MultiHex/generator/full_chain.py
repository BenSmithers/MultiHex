from MultiHex.generator import make_ridges
from MultiHex.generator import fill_land
from MultiHex.generator import sim_weather
from MultiHex.generator import biome_maker
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
    biome_maker.generate( size, name )

def full_sim( size, name ):
    make_ridges.generate( size, name )
    ridge_onward( size, name )

if __name__=='__main__':
    if sys.platform=='linux':
        basedir = os.path.join(os.path.expandvars('$HOME'),'.local','MultiHex')
    elif sys.platform=='darwin': #macOS
        basedir = os.path.join(os.path.expandvars('$HOME'),'MultiHex')
    elif sys.platform=='win32' or sys.platform=='cygwin': # Windows and/or cygwin. Not actually sure if this works on cygwin
        basedir = os.path.join(os.path.expandvars('%AppData%'),'MultiHex')
    else:
        raise NotImplementedError("{} is not a supported OS".format(sys.platform))
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    savedir = os.path.join(basedir, 'saves')
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    full_sim( 'cont', os.path.join( savedir, 'generated.hexmap' ))
