# MultiHex
A Hex-Map maker, editor, and interface by Ben Smithers.

This is an open-source MultiHex tool for (eventually) all your hex-map needs. 
It will always be open-source and always be freely available on github.
It's under active development and there are no official stable releases at the moment.
The `master` branch is kept stable (with a few known bugs), with experimental features being kept under the other branches. 

# Prerequesites

You will need PyQt5, Python 3, and numpy.
Ensure you install numpy and Qt for python 3, and not python 2! 
Python2 is unsupported (and won't work due to some changes in the way python handles class instance types between 2 and 3), and this is **known to fail in different verisons of Qt**. Because, again, there are big differences in the syntax used between PyQt4 and 5.

# Installing and Running

Installing is super easy. `cd` to some folder. `git clone git@github.com:BenSmithers/HexMap.git` to download it.

Then, `cd` into that new folder. Run `pwd`, copy the output, and open up your `~/.bashrc` file.
Add `export PYTHONPATH=$PYTHONPATH:/thing/you/just/copied` to the bottom of the that file. 

Now, open up a new terminal window, go to `/path/to/HexMap/HexMap` and run `./launch.py`. Congrats, you're in!

# Current Features

## World Generation

MultiHex currently supports a multi-step world generation system. 
When creating a new map, you have the option of 

a. Allowing *MultiHex* to seed the world with its own mountain ridges, and spawn the world from there, (recommended) or

b. Drawing out the mountainous ridge contours of your world, and letting *MultiHex* do the rest, or for the dedicated. (outdated)

c. Filling in all the dtails yourself, starting with just a blank canvas and creativity. (not working)

*MultiHex* uses a seeded algorithm to generate the world's topography and oceans. 
Then, it uses a 'nuanced' weather model to propagate storm systems across your new world to map out areas of intense rainfall and arid deserts. 

## World Editor

The master branch editor allows you to change Hexes and draw new biomes. An update to this interface is currently under development, see #11 for more details. 

## Civilization Editor

Allows the user to view and edit the civilizations on the map: locations (with multiple choices of icons), settlements, roadways, counties, and kingdoms (which are collections of counties). Currently uses template artwork for the buttons. 

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
