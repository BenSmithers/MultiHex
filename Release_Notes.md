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
