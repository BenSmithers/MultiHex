<p align="center">
  <img src="https://github.com/BenSmithers/MultiHex/blob/master/MultiHex/Artwork/wiki_images/multihex_logo.png" alt="MultiHex Logo" width="500" height="500">
</p>

# MultiHex
A Hex-Map maker, editor, and interface by Ben Smithers.

Get the latest release [here](https://github.com/BenSmithers/MultiHex/releases)!

This is an open-source MultiHex tool for (eventually) all your hex-map needs. 
It will always be open-source and always be freely available on github.
It's under active development and there are no official stable releases at the moment.
The `master` branch is kept stable (with a few known bugs), with experimental features being kept under the other branches. 

If you find bugs or would like to request a feature not on the issues list (or if you just want to let us know how we're doing), let us know on [this form](https://forms.gle/XXBaRJvRrmQyJXfV9). 

# Prerequesites

You will need PyQt5, Python 3, and numpy.
Ensure you install numpy and Qt for python 3, and not python 2! 
Python2 is unsupported (and won't work due to some changes in the way python handles class instance types between 2 and 3), and this is **known to fail in different verisons of Qt**. Because, again, there are big differences in the syntax used between PyQt4 and 5.

# Installing and Running

Installing is super easy. `cd` to some folder. `git clone git@github.com:BenSmithers/MultiHex.git` to download it.

Then, `cd` into that new folder. Run `pwd`, copy the output, and open up your `~/.bashrc` file.
Add `export PYTHONPATH=$PYTHONPATH:/thing/you/just/copied` to the bottom of the that file. 

Now, open up a new terminal window, go to `/path/to/MultiHex/MultiHex` and run `python3 ./main_file.pyw`. Congrats, you're in!

# Current Features

## World Generation

*MultiHex* currently supports a multi-step world generation system with multiple presets, and the option of customizing existing to your hearts content. 

<p align="center">
  <img src="https://github.com/BenSmithers/MultiHex/blob/master/MultiHex/Artwork/wiki_images/worldgen.PNG" alt="A screenshot of the MultiHex world generation dialogs" width="1082" height="752">
</p>

*MultiHex* uses a seeded algorithm to generate the world's topography and oceans. 
Then, it uses a 'nuanced' weather model to propagate storm systems across your new world to map out areas of intense rainfall and arid deserts. 

## World Editor

A fully-fledged terrain editor is in place that allows for drawing vast swaths of desert, grassland, forests, and more. 
Modifications of existing json files allows for easy addition of new hex climates with seamless integration into the world generation algorithm. 

<p align="center">
  <img src="https://github.com/BenSmithers/MultiHex/blob/master/MultiHex/Artwork/wiki_images/terrain_editor.PNG" alt="A screenshot of the MultiHex terrain editor" width="1082" height="752">
</p>

Users can also draw new rivers, inject perlin noise into climate-determining hex parameters, use the 'detailer' brush to finely-tune the climate at each hex, and draw bordered regions on the map for named geographic features.


## Civilization Editor

Allows the user to view and edit the civilizations on the map: locations (with multiple choices of icons), settlements, roadways, counties, and kingdoms (which are collections of counties).

<p align="center">
  <img src="https://github.com/BenSmithers/MultiHex/blob/master/MultiHex/Artwork/wiki_images/civ_editor.PNG" alt="A screenshot of the MultiHex civilization editor" width="1082" height="752">
</p>

# Future Plans

For a detailed list of planned features, or ways to contribute, see the issues list.

## Map Run Mode

A verison to be used as an over-land map in ttrpgs. 

* World Clock and Calendar. 
Keeps track of the days, the hours, the months and years. 
Quickly check the time of day, the light level, the seasons and the phase of the moon.
Time can be skipped forward to simulated down-time

* WeatherSim. 
A toy-model weather simulator will propagate storm systems across the world, after spawning them on occasion out in the ocean. 

* Entity tracking. Keep track of entities on the map, like a party in a ttrpg.
Allow the entities to travel plan travel across the map, to travel immeditely, or teleport. 
Turn the clock forward accordingly when travelling.

* Insta-Flavor text. What's it like on a certain hex *right now?* Using the world clock, local weather, hex features, and neighbor hex features, this will provided a breif description of this hex. 

* May want to add fog-of-war like feature to share maps with players
