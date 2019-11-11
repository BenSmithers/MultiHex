#include <hexmap.h>

namespace hexmap{
    //to be implemented 
    // hexes are tiled around one hex centered at origin

    Hexmap::Hexmap(){
		scaling_constant = 1.0;
    }

    void Hexmap::register_hex( Hex* hex ){
        std::map<uint64_t, Hex*>::iterator it = this->find( hex->get_id() );

        if( it == this->end() ){
            // no such entry is already there, so log it
            hex_catalogue->insert( hex->get_id(), hex );
        }else{
            // TODO
            // log a notice that the hex is already registered 
        }
    }
	
	void Hexmap::set_active_hex(uint64_t id){
		Hex* new_hex;
		try{
			new_hex = get_hex_with_id( id );
		}catch(InvalidHex& e){
			// log notice thingy, hex doesn't exist! 
		}
	}

    Hex* Hexmap::get_hex_with_id( uint64_t id ){
        std::map<uint64_t, Hex*>::iterator it = hex_catalogue.find( id );
        if ( it != hex_catalogue.end() ){
            return( hex_catalogue[id] );
        }else{
            throw InvalidHex();
        }
    }
	
	// takes a position in (x,y) space, returns the id for a hex there
	uint64_t get_id_from_point( double pos_x, double pos_y ){
		double trans_x = transformed_x(pos_x, pos_y);
		double trans_y = transformed_y(pos_x, pos_y);
		
		int32_t base_idx = 2*int(floor( trans_x/(2*rthree*scaling_constant)));
		int32_t base_idy =   int(floor( trans_y/(rthree*scaling_constant)));
		
		double rel_y = fmod( pos_y, rthree*scaling_constant);
		double rel_x = fmod( pos_x, 2*scaling_constant);
		bool line_h  = rel_y > rthree*scaling_constant*0.5;
		bool line_p  = rel_y > rthree*rel_x;
		bool line_n  = rel_y > (-1*rthree*rel_x +scaling_constant*rthree);
		bool line_n2 = rel_y > (-1*rthree*rel_x +3*scaling_constant*rthree);
		bool line_p2 = rel_y > (rthree*rel_x -2*scaling_constant*rthree);
		
		if (line_h){
			if (line_p){
				base_idy++;
			}else{
				base_idx++;
				if(line_n2){
					base_idx++;
				}
			}
		}else{
			if (line_n){
				base_idx++;
				if (!line_p2){
					base_idx++;
					base_idy--;
				}
				
			}
		}
		
		uint64_t id = ( base_idx << 32) | base_idy;
		return(id);
		
	}

}// namespace hexmap
