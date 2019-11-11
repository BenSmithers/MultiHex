#ifndef HEXMAP_H
#define HEXMAP_H

#include <point.h>
#include <hex.h>
#include <map>

namespace hexmap{
    class Hexmap{
        public:
            Hexmap();
			
			double scaling_constant;
            
            Hex* get_hex_with_id(int id);
            void register_hex(Hex* hex);
			Hex* get_active_hex(void){ return(active_hex); }
			void set_active_hex( int id );
			
        private:
			Hex* active_hex; 
            std::map<int, Hex*> hex_catalogue;
			
    };
}

#endif
