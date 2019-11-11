#ifndef POINT_H
#define POINT_H

namespace hexmap{

class Point{
		private:
			double x;
			double y;
		
		public:
			Point();
			Point(double xx, double yy);
		
			void reflect();
			double get_x(){ return x; }
			double get_y(){ return y; }
			
			//overloading some operators
			
			// allows adding two points together in the form of vector addition
			Point operator + (Point const &obj){
				Point new;
				new.x = this->x + obj.x;
				new.y = this->y + obj.y;
				return(new);
			}
			
			// allows multiplying a point by a double... scales each component by the scalar
			Point operator * (double scalar){
				Point new;
				new.x = (this->x)*scalar;
				new.y = (this->y)*scalar;
				return(new);
			}
			
			std::ostream& operator << (ostream& os, const Point& point){
				os << "(" << point.get_x() << "," << point.get_y() << ")";
				return(os);
			}
	};

}// namespace hexmap

#endif
