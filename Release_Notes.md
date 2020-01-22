## January XX 2020

### Additions

* Added the Civilization Editor GUI

* Added Entities: objects which can be placed on a HexMap

* Added Settlements

* Added Roads

* Added brushes for adding roads, settlements, and entities on a map

### Fixes and Changes

* Fixed issues with adding Points to the start of a path 

* Refined the layering and established protocols for future layering 

* Fixed the Path datastructure, and implemented a 'Path ID' system similar to the 

## December 18 2019

### Additions

* MCMC name generator for cooler, theme-appropriate names.

* Rivers and lakes are now created. 

### Fixes

* Fixed issue where removing hexes from reginos would sometimes mess up the region border

* Fixed issue where adding hex to region would _sometimes_ crash application

## December 1 2019

### Additions 

* Added Simple layering:
 Hexes < Regions < Brushes < Region Names 

* Region Labels look nicer 

* Moon phase functionality to clock object

* World generator now creates and names regions

### Fixes

* Unused buttons are disabled

* Fixed bug where you would try adding some hex to a region, remove the hex from another region, but then not be able to add to the region. Lead to conflics in some maps. 

* Fixed bug where hexid would be popped but the hex wouldn't be popped 

## November 29 2019

### Additions

* Can now assign region names.
They are drawn over the regions too. 

* Added region brush tool.

* Removed selector tool. Folded its functionality into the brushes. Right click (or Alt+Click) now draws with the brush and left click accesses the relevant selector.
Selects either a brush or a region, depending on what kind of brush you are using.

* Major changes to the world editor gui. 

* Drawing over a hex with the Hex Brush now replaces that hex, scales its color according to the altitude. 

* Main map will load in regions and draw them, if necessary. 

### Fixes

* Several fixes to the member functions of the region class. 

* Fixed the color oceans were drawn with. Now it matches the shallows. 

## November 28 2019

### Additions

* Added first working prototype of regions, and a prototype gui for drawing them 

* Added Release Notes

### Fixes

* gitignore actually ignores swap files

* main menu now only hides when a filename is specified, so it won't flash when you cancel the file dialog. 

* Point equality function now only checks for closeness, so floating point weirdness doesn't prevent an accurate test of equality. 

* clicker controls now control a "drop" function when swapping tools. 
Helps for generalizing to any number of tools for a CC 
