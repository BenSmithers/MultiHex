#ifndef HEX_HEAD
#define HEX_HEAD

#include <point.h> 
#include <vector>
#include <exception> //custom exceptions for the hexes
#include <math.h> //adds square root, fmod function, floor

namespace hexmap{
	
	// calculate sqrt(3) once so we don't have to do it a lot
	static const double rthree = sqrt(3);
	static const double backup_radius = 1.0 

	class Hex{
		public:
			// hex constructors
			Hex();
			Hex(Point ccenter);
			Hex(Point ccenter, double rrad);
			Hex(Point ccenter, double* rrad);
			
			// some info-giving functions
            double  get_radius(void){return (*radius);} //evaluate the pointer! 
            Point   get_center(void){return center;}
            uint64_t get_id(void){return id;}
			
		private:
			double* radius; //just a pointer to where the radius actually is stored
			//				 this should be to the hexmap's scaling constant
			Point center;
            uint64_t id;
            

			//reeeaaaally gotta keep these private 
			Point vertices[6];
			void construct_vertices();
			void construct_id();
            
            // a list of pointers to the hexes neighboring this one 
            Hex* neighbors[6];
			
	};
	
	// Hex-related Exceptions
	struct InvalidHex : public std::exception{
		const char * what () const throw (){
			return("Invalid Hex ID");
		}
	}
	

} // end namespace hex

#endif
