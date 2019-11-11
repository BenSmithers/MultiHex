#include <hex.h>

namespace hexmap{
		
	//Hex constructors
	Hex::Hex(){
		Point center(0.0,0.0);
		radius		= &backup_radius;
		construct_vertices();
		construct_id();
	}
	
	Hex::Hex(Point ccenter){
		center = ccenter;
		radius = &backup_radius;
		construct_vertices();
		construct_id();
	}
	
	Hex::Hex(Point ccenter, double rrad){
		center = center;
		radius = &rrad;
		construct_vertices();
		construct_id();
	}
	
	Hex::Hex(Point ccenter, double* rrad){
		center = center;
		radius = rrad;
		construct_vertices();
		construct_id();
	}

	
	// Hex utility function. Fills the verticecs vector 
	void Hex::construct_vertices(){
		// these are built assuming the radius goes from center to a vertex
		// 		and that the hex is aligned "horizontally": top and bottom are parallel to horiz
		vertices[0] = center + Point(-0.5, 0.5*rthree)*(*radius);
		vertices[1] = center + Point(0.5,  0.5*rthree)*(*radius);
		vertices[2] = center + Point(1.0, 0.0)*(*radius);
		vertices[3] = center + Point(0.5, -0.5*rthree)*(*radius);
		vertices[4] = center + Point(-0.5, -0.5*rthree)*(*radius);
		vertices[5] = center + Point(-1.0, 0.0)*(*radius);
	}
	
	void Hex::construct_id(){
		// use location of center point to get ID 
		Point transf = transformed_point( &(this->center) );
		// these support a map ~4 billion hexes tall/wide 
		int32_t id_x = int(floor(rthree*( transf.get_x() )/(*(this->radius)) + 0.5));
		int32_t id_y = int(floor(rthree*( transf.get_y() )/(*(this->radius)) + 0.5));
		
		// concatenates binary representations of the x-id and y-id
		// first 16 bits from idx, last 16 bits from idy. Written to 64 bit id, fully positive 
		this->id = ( id_x << 32) | id_y;
		
	}
	
	
	// these two functions fransform x,y into a new coordinate system the ID system is based off of 
	double transformed_x(double x, double y=0.0){
		// y-value not used, but keeping default value for symmetry with transformed_y function
		return( x/rthree ); //rthree is sqrt(3)
	}
	double transformed_y(double x, double y){
		return( y - x/rthree );
	}
	Point transformed_point( Point* ppoint ){ //returns a point in the transformed coordinates
		double new_x = ppoint->get_x()/rthree ;
		double new_y = ppoint->get_y() - ( ppoint->get_x()/rthree);
		Point new_point( new_x, new_y );
		return( new_point );
	}
	
} // end namespace hexmap
