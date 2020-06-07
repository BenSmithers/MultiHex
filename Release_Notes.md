## June 05 2020 (v0.3.0)

### Additions

**Major:**

* added new GUI to support world generation with both presets and advanced generation parameters. 

* multithreading for world generation so the gui doesn't sieze up and act non-responsive

**Minor:**

* added window icon for MultiHex 

* Users can now change the color of counties (and in effect kingdoms) 

### Changes

**Major:**

* totally reworked the GUIs! Now allows for rapid switching between the different editors

* Updated the civilization toolbar artwork, removed old unused buttons

**Minor:**

* Dramatically reduced file sizes 

* Starting to draw a path from the end of an existing path will allow the continuing of the existing path (applies to rivers, roads)

* changed structure of json file for world generation. Each parameter should have a correlated entry with its description. 

## Bug Fixes

* Fixed issue where tributaries were not being drawn

* Fixed problem where a spaceritem had the same layout location as a button, causing an obnoxious warning

* Fixed issue where the Hex Brushes outline wouldn't be removed when switching to a new tool

* Several other minor bugfixes 

## April 20ish 2020 (v0.2.0)

### Additions

**Major:**

* Hexmaps are now updated as new features are added. There are chained functions for loading old Hexmaps and uploading them to the newest version. 

* A tilesets file has been added describing Hex climates; these specify a color and central values for attributes describing the climate. 
The tilesets and climate system are parameter-agnostic to allow for easier expansion to other tilesets or map types

* Added a system for injecting perlin noise into any parameter of the map

* Added "Detailer" brush for raising/lowering temperatures, altitudes, rainfall patterns 

* Biome border colors can be chosen from a colorpicker 

* Climates can be recalculated

* Users can now draw rivers and tributaries 

**Minor**

* Added (beta) Heatmaps for any Hex property

* Added a clock system for use in the map usability update 

* Added 3D and ND Points. Smallest dimensionality should be used to save space! 

* Added some unit tests. A future update should add more. 

* Biome names can be auto-generated in the editor

### Changes

* Better support for more Hex climates /  colors! 

* Changed the controls for the region brushes 

* Hexes climates are now determined through a method 

* User can choose a biome's color

* more docstrings were added

* More code reuse! 

* User can toggle whether biome names/borders are shown 

* Added script for generating docs

* New button icons! 

### Fixes

* fixed bug where rivers would be accepted with length 1 and no tributaries

## January 20 2020

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
