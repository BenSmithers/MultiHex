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
