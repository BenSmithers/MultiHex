# Idea

Develop a generator for civilizations and roads 

# Requirements

This will require a few new features. 

 - Resources. 
Some ``resources" will need to be scattered around the map in a logical way. 
Things necessary for many historical civilizations: woodlands (might just be associated with the actual forest hexes), iron, copper (tin?), coal, etc. 

- More Hex parameters. 
Fertility of a hex should also be a thing; this might just need to be a new paramter like altitude and temperature.
The fertility is largely dependent on the history of the land itself, like the chemical composition. 
Might actually want to do some research on this... 
but, fertility could probably just be decided based on some perlin noise over the whole map.
Fertility assignment could be assigned at hex generation. 

- Pathing. 
MultiHex needs to know how to calculate the quickest path between two hexes. 
This should be dependent on the existence of roads and the altitude differences between hexes.
This should be SMART. 
Consider A* pathing? 
Facilitating this might require that a path-follower caches the path (A series of hexIDs) before leaving towards a destination. 
May need a get-cost function for distances between two hexes? 
Individual hexes will have an associated cost.
Travelling between hexes A and B will have a cost of `0.5*(C_a + C_b)` 

- Rework tension property of governments.
There should be two sources of tension: differing values between a people and their government, and diverse demographics in non-peaceful or accepting settlements. 

# Functionality 

## Goal:

Generate counties, kingdoms, roads, and locations until some criteria is met. 

## Functionality 

### Step 1: Seeding

First, some `n_civs` will be seeded around the world.
This will be done by creating this number of settlements with randomly assigned values, 20 people (80% human, 20% dwarf, 20% elf?  -- all or nothing, but with these probabilities). 
A county will be made around the settlement with a name relevant to that of the settlement. 

### Step 2: Propagation

Each "turn" will represent 1 year. 
In each turn, a few things can happen. 

Settlement actions 
 - Emmigrate. 
If tensions are high, or a population has reached its maximum based on the available resources, a group of people (10-25?) should form a mobile and leave. 
 - Build?
Provided the resources are available, it could try making a farm or a tavern, or a harbor, etc. 

Settlement population should grow each turn. 
This should be proportional to the difference between the curent population and the population max (calculated by all the potential for farming for the sum of all th hexes in the local county, divided by the number of settlements). 
It's a logistic curve.
Maximum population growth per year should be like... 0.5-5% 
