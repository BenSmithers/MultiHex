from HexMap.generator import make_ridges
from HexMap.generator import fill_land
from HexMap.generator import sim_weather

def full_sim( size, name ):
    make_ridges.generate( size, name )
    fill_land.generate(size, name)
    sim_weather.generate( size, name )

def ridge_onward( size, name ):
    fill_land.generate( size, name )
    sim_weather.generate( size, name )

if __name__=='__main__':
    full_sim( 'cont', '../saves/generated.hexmap' )
