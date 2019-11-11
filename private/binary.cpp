#include <hexmap.h>
#include <hex.h>
#include <point.h>

#include <iostream>

int main(){
	
	Point center_one( 0.0, 0.0);
	Hex main_hex( center_one, 2.0 );
	
	std::cout << "Radius: " << main_hex.get_radius() << std::endl;
	std::cout << "Center: " << main_hex.get_center() << std::endl;
	
	
	return(0);
}